from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_mysqldb import MySQL
import bcrypt, os

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'b9tnqejctcawupra3lnn-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'u9behnvew7j2blv2'
app.config['MYSQL_PASSWORD'] = 'XLatL7wv5mhNiKZzyskZ'
app.config['MYSQL_DB'] = 'b9tnqejctcawupra3lnn'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=10, ping_interval=5)


@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', [usuario])
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Usuario ya registrado', 'danger')
        else:
            password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO usuarios (usuario, password) VALUES (%s, %s)', (usuario, password))
            mysql.connection.commit()
            flash('Usuario registrado con éxito', 'success')

        cursor.close()
        return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', [usuario])
        user = cursor.fetchone()
        cursor.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session['usuario'] = usuario
            return redirect(url_for('chat'))
        
        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/chat')
def chat():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    # Obtener contactos del usuario
    cursor.execute('SELECT contacto_id FROM contactos WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = %s)', (session['usuario'],))
    contactos = cursor.fetchall()
    contactos_info = []
    for contacto in contactos:
        cursor.execute('SELECT usuario FROM usuarios WHERE id = %s', (contacto[0],))
        contactos_info.append(cursor.fetchone())

    # Obtener grupos del usuario
    cursor.execute('SELECT grupos.nombre FROM grupos JOIN usuarios_grupos ON grupos.id = usuarios_grupos.grupo_id WHERE usuarios_grupos.usuario_id = (SELECT id FROM usuarios WHERE usuario = %s)', (session['usuario'],))
    grupos = cursor.fetchall()

    cursor.close()
    return render_template('chat.html', contactos=contactos_info, grupos=grupos, usuario=session['usuario'])





@socketio.on('join')
def handle_join(data):
    join_room(data['room'])
    

@socketio.on('join_chat')
def handle_join_chat(data):
    usuario = data['usuario']
    contacto = data.get('contacto')

    if contacto:  # Chat individual
        room = f"{min(usuario, contacto)}-{max(usuario, contacto)}"
    else:  # Chat grupal
        room = data['room']

    join_room(room)
    socketio.emit('chat_joined', {'room': room}, room=room)



@socketio.on('send_message')
def handle_send_message(data):
    room = data.get('room')  # e.g., 'user1-user2' o 'nombre_del_grupo'
    message = data.get('message')
    usuario = data.get('usuario')

    if room and message and usuario:
        cursor = mysql.connection.cursor()

        if '-' in room:
            # Chat individual
            users = room.split('-')
            if len(users) != 2:
                cursor.close()
                return
            user1, user2 = users
            sender = usuario
            receiver = user2 if user1 == usuario else user1

            # Obtener IDs de usuario
            cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (sender,))
            sender_id = cursor.fetchone()
            if not sender_id:
                cursor.close()
                return
            sender_id = sender_id[0]

            cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (receiver,))
            receiver_id = cursor.fetchone()
            if not receiver_id:
                cursor.close()
                return
            receiver_id = receiver_id[0]

            # Insertar mensaje en la tabla 'mensajes'
            cursor.execute(
                'INSERT INTO mensajes (remitente_id, receptor_id, mensaje) VALUES (%s, %s, %s)',
                (sender_id, receiver_id, message)
            )
            mysql.connection.commit()

        else:
            # Chat grupal
            group_name = room
            # Obtener ID del grupo
            cursor.execute('SELECT id FROM grupos WHERE nombre = %s', (group_name,))
            group = cursor.fetchone()
            if not group:
                cursor.close()
                return
            group_id = group[0]

            # Obtener ID del remitente
            cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (usuario,))
            sender_id = cursor.fetchone()
            if not sender_id:
                cursor.close()
                return
            sender_id = sender_id[0]

            # Insertar mensaje en la tabla 'mensajes' con grupo_id
            cursor.execute(
                'INSERT INTO mensajes (remitente_id, grupo_id, mensaje) VALUES (%s, %s, %s)',
                (sender_id, group_id, message)
            )
            mysql.connection.commit()

        cursor.close()

        # Emitir el mensaje a la sala correspondiente
        socketio.emit('receive_message', {
            'room': room,
            'usuario': usuario,
            'message': message
        }, room=room)

@socketio.on('message')
def handle_message(data):
    send(f"{data['usuario']}: {data['mensaje']}", room=data['room'])
    
@socketio.on('leave')
def handle_leave(room):
    leave_room(room)
    
    
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    # Obtener todos los usuarios registrados excepto el actual
    cursor.execute('SELECT usuario FROM usuarios WHERE usuario != %s', (session['usuario'],))
    usuarios = cursor.fetchall()
    
    # Obtener el id del usuario actual
    cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (session['usuario'],))
    usuario_id = cursor.fetchone()[0]
    
    # Obtener los contactos del usuario actual
    cursor.execute('SELECT usuario FROM usuarios '
                   'JOIN contactos ON usuarios.id = contactos.contacto_id '
                   'WHERE contactos.usuario_id = %s', (usuario_id,))
    contactos = [row[0] for row in cursor.fetchall()]  # Obtener solo los nombres de usuario
    cursor.close()
    
    return render_template('usuarios.html', usuarios=usuarios, contactos=contactos, usuario=session['usuario'])



@app.route('/agregar_contacto', methods=['POST'])
def agregar_contacto():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    contacto = data['contacto']

    cursor = mysql.connection.cursor()
    # Verificar si el contacto existe en la base de datos de usuarios
    cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (contacto,))
    contacto_id = cursor.fetchone()

    if contacto_id:
        # Obtener el id del usuario actual
        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (session['usuario'],))
        usuario_id = cursor.fetchone()
        
        # Verificar si el contacto ya está agregado
        cursor.execute('SELECT * FROM contactos WHERE usuario_id = %s AND contacto_id = %s', (usuario_id[0], contacto_id[0]))
        if cursor.fetchone():
            message = f'El contacto {contacto} ya está agregado.'
        else:
            # Agregar el contacto si no está duplicado
            cursor.execute('INSERT INTO contactos (usuario_id, contacto_id) VALUES (%s, %s)', (usuario_id[0], contacto_id[0]))
            mysql.connection.commit()
            message = f'Contacto {contacto} agregado correctamente.'
    else:
        message = 'Contacto no encontrado.'

    cursor.close()
    return {'message': message}

@app.route('/eliminar_contacto', methods=['POST'])
def eliminar_contacto():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    contacto = data['contacto']

    cursor = mysql.connection.cursor()
    # Verificar si el contacto existe en la base de datos de usuarios
    cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (contacto,))
    contacto_id = cursor.fetchone()

    if contacto_id:
        # Obtener el id del usuario actual
        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (session['usuario'],))
        usuario_id = cursor.fetchone()
        
        # Verificar si el contacto está agregado antes de eliminarlo
        cursor.execute('SELECT * FROM contactos WHERE usuario_id = %s AND contacto_id = %s', (usuario_id[0], contacto_id[0]))
        if cursor.fetchone():
            # Eliminar el contacto
            cursor.execute('DELETE FROM contactos WHERE usuario_id = %s AND contacto_id = %s', (usuario_id[0], contacto_id[0]))
            mysql.connection.commit()
            message = f'Contacto {contacto} eliminado correctamente.'
        else:
            message = f'El contacto {contacto} no está en su lista de contactos.'
    else:
        message = 'Contacto no encontrado.'

    cursor.close()
    return {'message': message}

@socketio.on('create_group')
def handle_create_group(data):
    group_name = data['group_name']
    usuario = data['usuario']

    # Lógica para crear un nuevo grupo en la base de datos (si no existe)
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM grupos WHERE nombre = %s', (group_name,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO grupos (nombre, creador) VALUES (%s, %s)', (group_name, usuario))
        mysql.connection.commit()
    cursor.close()

    # Emitir el evento a todos los usuarios conectados
    socketio.emit('group_created', {'group_name': group_name}, to='/')

@socketio.on('join_group')
def handle_join_group(data):
    group_name = data['group_name']
    usuario = data['usuario']
    
    # Asegúrate de unir al usuario a la sala del grupo
    join_room(group_name)
    socketio.emit('user_joined', {'usuario': usuario, 'group_name': group_name}, room=group_name)



@app.route('/grupos')
def grupos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    # Obtener todos los grupos
    cursor.execute('SELECT nombre FROM grupos')
    grupos = cursor.fetchall()

    # Obtener los grupos que el usuario ha agregado
    cursor.execute('SELECT grupos.nombre FROM grupos JOIN usuarios_grupos ON grupos.id = usuarios_grupos.grupo_id WHERE usuarios_grupos.usuario_id = (SELECT id FROM usuarios WHERE usuario = %s)', (session['usuario'],))
    grupos_agregados = [row[0] for row in cursor.fetchall()]  # Convertir los resultados en una lista de nombres

    cursor.close()
    return render_template('grupos.html', grupos=grupos, grupos_agregados=grupos_agregados)


@app.route('/crear_grupo', methods=['POST'])
def crear_grupo():
    data = request.get_json()
    nombre = data['nombre']
    usuario = session['usuario']

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM grupos WHERE nombre = %s', (nombre,))
    if cursor.fetchone():
        message = 'El grupo ya existe.'
    else:
        cursor.execute('INSERT INTO grupos (nombre, creador) VALUES (%s, %s)', (nombre, usuario))
        mysql.connection.commit()
        message = 'Grupo creado exitosamente.'

    cursor.close()
    return {'message': message}


@app.route('/eliminar_grupo', methods=['POST'])
def eliminar_grupo():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    nombre = data['nombre']

    cursor = mysql.connection.cursor()
    # Verificar si el grupo existe
    cursor.execute('SELECT id FROM grupos WHERE nombre = %s', (nombre,))
    grupo_id = cursor.fetchone()

    if grupo_id:
        # Obtener el id del usuario actual
        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (session['usuario'],))
        usuario_id = cursor.fetchone()[0]

        # Eliminar al usuario del grupo
        cursor.execute('DELETE FROM usuarios_grupos WHERE usuario_id = %s AND grupo_id = %s', (usuario_id, grupo_id[0]))
        mysql.connection.commit()
        message = 'Grupo eliminado correctamente.'
    else:
        message = 'El grupo no existe.'

    cursor.close()
    return {'message': message}

@app.route('/agregar_grupo', methods=['POST'])
def agregar_grupo():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    nombre = data['nombre']

    cursor = mysql.connection.cursor()
    # Verificar si el grupo existe
    cursor.execute('SELECT id FROM grupos WHERE nombre = %s', (nombre,))
    grupo_id = cursor.fetchone()

    if grupo_id:
        # Obtener el id del usuario actual
        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (session['usuario'],))
        usuario_id = cursor.fetchone()[0]

        # Verificar si el usuario ya está en el grupo
        cursor.execute('SELECT * FROM usuarios_grupos WHERE usuario_id = %s AND grupo_id = %s', (usuario_id, grupo_id[0]))
        if cursor.fetchone():
            message = 'Ya estás en este grupo.'
        else:
            # Agregar al usuario al grupo
            cursor.execute('INSERT INTO usuarios_grupos (usuario_id, grupo_id) VALUES (%s, %s)', (usuario_id, grupo_id[0]))
            mysql.connection.commit()
            message = 'Grupo agregado correctamente.'
    else:
        message = 'El grupo no existe.'

    cursor.close()
    return {'message': message}

@app.route('/get_messages', methods=['GET'])
def get_messages():
    if 'usuario' not in session:
        return {'error': 'Unauthorized'}, 401

    room = request.args.get('room')
    if not room:
        return {'error': 'No room specified'}, 400

    cursor = mysql.connection.cursor()

    if '-' in room:
        # Chat individual
        users = room.split('-')
        if len(users) != 2:
            cursor.close()
            return {'error': 'Invalid room format'}, 400

        user1, user2 = users

        # Obtener IDs de usuarios
        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (user1,))
        user1_id = cursor.fetchone()
        if not user1_id:
            cursor.close()
            return {'error': f'User {user1} not found'}, 404
        user1_id = user1_id[0]

        cursor.execute('SELECT id FROM usuarios WHERE usuario = %s', (user2,))
        user2_id = cursor.fetchone()
        if not user2_id:
            cursor.close()
            return {'error': f'User {user2} not found'}, 404
        user2_id = user2_id[0]

        # Consultar mensajes
        cursor.execute('''
            SELECT u.usuario, m.mensaje, m.timestamp
            FROM mensajes m
            JOIN usuarios u ON m.remitente_id = u.id
            WHERE (m.remitente_id = %s AND m.receptor_id = %s)
               OR (m.remitente_id = %s AND m.receptor_id = %s)
            ORDER BY m.timestamp ASC
        ''', (user1_id, user2_id, user2_id, user1_id))

    else:
        # Chat grupal
        group_name = room
        # Obtener ID del grupo
        cursor.execute('SELECT id FROM grupos WHERE nombre = %s', (group_name,))
        group = cursor.fetchone()
        if not group:
            cursor.close()
            return {'error': f'Group {group_name} not found'}, 404
        group_id = group[0]

        # Consultar mensajes del grupo
        cursor.execute('''
            SELECT u.usuario, m.mensaje, m.timestamp
            FROM mensajes m
            JOIN usuarios u ON m.remitente_id = u.id
            WHERE m.grupo_id = %s
            ORDER BY m.timestamp ASC
        ''', (group_id,))

    messages = cursor.fetchall()
    cursor.close()

    # Convertir los mensajes a una lista de diccionarios
    message_list = []
    for msg in messages:
        message_list.append({
            'sender': msg[0],
            'message': msg[1],
            'timestamp': msg[2].strftime('%Y-%m-%d %H:%M:%S')
        })

    return {'messages': message_list}

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
