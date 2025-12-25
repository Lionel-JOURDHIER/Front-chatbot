from nicegui import app, ui, run
import asyncio
import requests

# 1. On déclare le dossier contenant le CSS (ici le dossier courant '.')
app.add_static_files('/static', '.')
app.add_static_files('/static', './assets')

# 2. On injecte le lien CSS dans le header HTML
ui.add_head_html('<link rel="stylesheet" href="/static/style.css">')

settings = {
    'mode': 'Detailed Analysis',
    'sentiment': True,   # État initial du switch Sentiment
    'translation': True # État initial du switch Traduction
}     

SENTIMENT_CORRESP = {
    "1 star": f'/static/assets/colere.png',
    "2 stars": f'/static/assets/pas_content.png',
    "3 stars": f'/static/assets/neutre.png',
    "4 stars": f'/static/assets/heureux.png',
    "5 stars": f'/static/assets/adore.png'
}

async def ajouter_bulle(texte, traduction, sentiment, est_utilisateur=True):
    with chat_container:
        align = 'justify-end' if est_utilisateur else 'justify-start'
        # On utilise nos classes CSS au lieu de Tailwind
        bubble_class = 'bubble-user' if est_utilisateur else 'bubble-ai'
        bubble_class_trad = 'bubble-user-trad' if est_utilisateur else 'bubble-ai-trad'
        
        with ui.row().classes(f'w-full {align} items-end gap-2'):
            if not est_utilisateur and settings['sentiment']:
                with ui.avatar().classes('sentiment').style('background-color: #F6F1EE !important'):
                    ui.image(sentiment).classes('w-full h-full object-cover')
            
            with ui.column().classes(f'{align} items-end gap-1'):
                with ui.row().classes(bubble_class + ' max-w-md shadow-sm gap-0'):
                    label_message = ui.label('').classes('text-sm')
                    if est_utilisateur : 
                        label_message.set_text(texte)
                    else : 
                        label_message.text = "" # On s'assure qu'il est vide au départ
                        for lettre in texte:
                            label_message.text += lettre
                            await asyncio.sleep(0.02) # Vitesse de frappe (20ms par lettre)
                            await scroll_down()
                if settings['translation'] and traduction:
                    with ui.row().classes(bubble_class_trad + ' max-w-md shadow-sm gap-0'):
                        with ui.row().classes('items-baseline mt-1 opacity-80'):
                                ui.label('TRADUCTION :').classes('translation-label')
                                ui.label(traduction).classes('translation-text')

            if est_utilisateur and settings['sentiment']:
                with ui.avatar().classes('sentiment').style('background-color: #6e594b !important'):
                    ui.image(sentiment).classes('w-full h-full object-cover')

def send_get_request(url: str):
    # Cette ligne "bloque" le thread où elle s'exécute
    response = requests.get(url)
    return response.json()

def send_post_request(url, payload):
    # On effectue le POST de manière synchrone
    response = requests.post(url, json=payload)
    return response.json()

async def scroll_down():
    await asyncio.sleep(0.01)
    area.scroll_to(percent=1.0)
    return True

async def envoyer_message():
    label_bienvenue.set_visibility(False)
    message = saisie.value.strip()
    user_data = {"texte" : message}
    if message:
        # 1. On vide le champ immédiatement
        saisie.value = ''
        # 2. On ajoute un spinner pour faire patienter
        with chat_container:
            with ui.row().classes(f'fit items-center gap-1 justify-end') as spinner_row:
                with ui.card().classes('bubble-user'):
                    ui.spinner('dots', size='xs', color="#faf7f1")
            await scroll_down()
        # 3. On attend le retour de l'API
            sentiment_json = await run.io_bound(
            send_post_request, 
            'http://127.0.0.1:8090/analyse/', 
            user_data
        )
            
            sentiment_image = SENTIMENT_CORRESP.get(sentiment_json["label"], "")

            traduction_json = await run.io_bound(
            send_post_request, 
            'http://127.0.0.1:8090/translate_fr_en/', 
            user_data
        )
        # 4. On retire le spinner
            chat_container.remove(spinner_row)
        # 5. On ajoute la bulle    
            await ajouter_bulle(message, traduction_json['translated_text'], sentiment_image ,est_utilisateur=True)
        # 6. On attend un tout petit peu que le message apparaisse pour scroller en bas
        await scroll_down()
        # 7. On affiche le spinner pour le chatbot
        with chat_container:
            with ui.row().classes(f'fit items-center gap-1 justify-start') as spinner_row:
                with ui.card().classes('bubble-ai'):
                    ui.spinner('dots', size='xs', color="#321f19")
            await scroll_down()
        # 8. On attend le retour de l'API
            response_json = await run.io_bound(
            send_post_request, 
            'http://127.0.0.1:8090/chatbot/', 
            user_data)
            response_sentiment_image = SENTIMENT_CORRESP.get(response_json["label"], "")
        # 9. On retire le spinner_ai
            chat_container.remove(spinner_row)
        # 10. On ajoute la bulle ia  
            await ajouter_bulle(response_json['response'], response_json['translated_text'], response_sentiment_image, est_utilisateur=False)
            await scroll_down()

async def effet_machine_a_ecrire():
    texte_complet = "Bienvenue dans votre application d'agent conversationnel : vous pouvez commencer en entrant un texte dans la zone blanche en bas."
    label_bienvenue.text = "" # On s'assure qu'il est vide au départ
    
    for lettre in texte_complet:
        label_bienvenue.text += lettre
        await asyncio.sleep(0.02) # Vitesse de frappe (50ms par lettre)

# --- Dans ton Layout ---
# On place le label avec ta police "écriture main" définie plus tôt


# --- Layout ---
# Header
with ui.header(elevated=True).classes('header'):
    with ui.row().classes('w-full justify-between items-center'):
        # Bloc de gauche
        with ui.row().classes('items-center'):
            with ui.button(on_click=lambda: drawer.toggle(), icon='menu') \
                .props('flat round color=brown-10'): 
                ui.tooltip('Menu').classes('bulle_info')
            ui.label('Sidora Chatbot').classes('text-2xl font-bold') \
                .classes('text-xl tracking-widest uppercase text-brown-8')
        # Bloc de droite
        with ui.row().classes('items-center'):
            with ui.switch('Sentiment') \
                .props('color="brown" dense') \
                .bind_value(settings, 'sentiment'):
                ui.tooltip('Afficher ou non les sentiments').classes('bulle_info')
            with ui.switch('Traduction') \
                .props('color="brown" dense') \
                .bind_value(settings, 'translation'):
                ui.tooltip('Afficher ou non les traductions').classes('bulle_info')

# Menu à gauche
with ui.left_drawer(value=False,fixed=True).style('background-color: #faf7f1') as drawer:
    with ui.column().classes('w-full q-pa-md gap-2'):
        ui.label('MENU').classes('text-xs text-brown-8 font-bold')
        with ui.link('Nouvelle conversation', '/chatbot/').classes('menu-link'):
            ui.tooltip("Afficher la page chatbot").classes('bulle_info')
        with ui.link('Connexions', '/connections').classes('menu-link'):
            ui.tooltip('Afficher la page de connexion').classes('bulle_info')
        ui.label('HISTORIQUE').classes('text-xs text-brown-8 font-bold my-2')
        
        history = ["Analyse de données", "Correction Bug Python", "Plan de voyage"]

with ui.card().tight().classes('moka-card'):  
    # Zone de Chat
    with ui.scroll_area().classes('w-full h-[500px]') as area:
    # On met une colonne à l'intérieur pour l'espacement des bulles (gap-8)
        chat_container = ui.column().classes('w-full max-w-[800px] mx-auto px-4 py-4')
        label_bienvenue = ui.label('').classes('titre-main text-lg mb-4 mx-8') \
            .classes('text-xl tracking-widest text-brown-8')

        # On lance l'animation dès que la page est prête
        ui.timer(0.1, effet_machine_a_ecrire, once=True)

    # Input
    with ui.row().classes('w-full p-6 bg-#D9C4BA items-center'):
        with ui.row().classes('w-full items-center bg-stone-50 border rounded-full px-5 py-2'):
            saisie = ui.textarea(placeholder='Veuillez écrire votre message ici...')\
                .props('borderless autogrow')\
                .classes('flex-grow')\
                .style('color: #FF0000 !important; font-size: 1rem; font-weight: 500;')\
                .on('keydown.enter.prevent', lambda: envoyer_message())
    # Correction ici : on utilise une lambda pour récupérer la valeur au clic
            with ui.button(icon='send', on_click=lambda: envoyer_message()) \
                .props('round')\
                .style('background-color: #6e594b !important'):
                ui.tooltip('Envoyer').classes('bulle_info')
    

ui.run()