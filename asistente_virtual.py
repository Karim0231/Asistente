import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

#opciones de idioma de voz
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

#Escuchar microfono y devolver el audio como texto
def transformar_audio_en_texto():
    #almacenar el recognizer en variable
    r = sr.Recognizer()

    #configurar el microfono
    with sr.Microphone() as origen:
        
        #tiempo de espera
        r.pause_threshold = 0.8

        #informar que empezo la grabacion
        print("ya puedes hablar")

        #guardar lo que escuches en audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language = "es-mx")

            #prueba que pudo ingresar
            print("Dijiste: " + pedido)

            #devolver pedido
            return pedido
        
        #en caso de no entender el audio
        except sr.UnknownValueError:
            #prueba de que no entendio el audio
            print("ups, no entendí")

            #devolver error
            return "sigo esperando"
        
        #en caso de no resolver el pedido
        except sr.RequestError:
            #prueba de que no entendio el audio
            print("ups, no hay servicio")

            #devolver error
            return "sigo esperando"
        
        #error inesperado
        except:
            #prueba de que no entendio el audio
            print("ups, algo ha salido mal")

            #devolver error
            return "sigo esperando"
        
#Funcion para que el asistente pueda hablar
def hablar(mensaje):

    #Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#Informar el dia de la semana
def pedir_dia():

    #crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    #crear una variable para el dia de la semana 
    dia_semana = dia.weekday()
    print(dia_semana)

    #diccionario con los dias de la semana
    calendario = {0:'Lunes',
                  1:'Martes',
                  2:'Miércoles',
                  3:'Jueves',
                  4:'Viernes',
                  5:'Sábado',
                  6:'Domingo'}
    
    #decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

#informar hora
def pedir_hora():

    #crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    #decir la hora 
    hablar(hora)

#funcion saludo inicial
def saludo_inicial():

    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen dia'
    else:
        momento = 'Buenas tardes'


    #decir el saludo
    hablar(f'{momento}, soy Sara, tu asistente personal. Por favor, dime en que te puedo ayudar')

#funcion central del asistente 
def pedir_cosas():

    #activar el saludo inicial
    saludo_inicial()

    #variable de corte
    comenzar = True

    #loop central 
    while comenzar:

        #activar el micro y guardar el pedido en un string 
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences = 1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar(f'Ya comienzo a reproducir el video')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try: 
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, en precio de {accion} es {precio_actual}')
                continue
            except:
                hablar("Perdon pero no la encontré")
                continue
        elif 'adios' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break


pedir_cosas()

#Ver voces de tus dispositivos
#engine = pyttsx3.init()
#for voz in engine.getProperty('voices'):
    #print(voz)