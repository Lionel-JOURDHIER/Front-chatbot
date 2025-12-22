from nicegui import app, ui
import asyncio

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

def ajouter_bulle(texte, traduction, sentiment, est_utilisateur=True):
    with chat_container:
        align = 'justify-end' if est_utilisateur else 'justify-start'
        # On utilise nos classes CSS au lieu de Tailwind
        bubble_class = 'bubble-user' if est_utilisateur else 'bubble-ai'
        spinner = ui.spinner('dots',size='l', color='brown-7')
        asyncio.sleep(5)
        chat_container.remove(spinner)
        with ui.row().classes(f'w-full {align} items-end gap-3'):
            
    

            if not est_utilisateur and settings['sentiment']:
                with ui.avatar().classes('sentiment').style('background-color: #F6F1EE !important'):
                    ui.image(sentiment).classes('w-full h-full object-cover')
            
            with ui.column().classes(bubble_class + ' max-w-md shadow-sm'):
                ui.label(texte).classes('text-sm')
                
                if settings['translation'] and traduction:
    # Pas de séparateur ici
                    # with ui.column().classes('w-full bg-black/5 p-2 rounded'): # Un léger voile sombre
                    with ui.row().classes('items-baseline mt-1 opacity-80'):
                            ui.label('TRADUCTION :').classes('translation-label')
                            ui.label(traduction).classes('translation-text')

            if est_utilisateur and settings['sentiment']:
                with ui.avatar().classes('sentiment').style('background-color: #6e594b !important'):
                    ui.image(sentiment).classes('w-full h-full object-cover')
        

async def envoyer_message():
    label_bienvenue.set_visibility(False)
    message = saisie.value.strip()
    if message:
        # 1. On ajoute la bulle
        ajouter_bulle(message, "I speak english", f'/static/assets/adore.png',est_utilisateur=True)
        # 2. On vide le champ immédiatement
        ajouter_bulle(message, "I speak english", f'/static/assets/colere.png',est_utilisateur=False)
        ajouter_bulle(message, "I speak english", f'/static/assets/heureux.png',est_utilisateur=False)
        ajouter_bulle(message, "I speak english", f'/static/assets/neutre.png',est_utilisateur=True)
        ajouter_bulle(message, "I speak english", f'/static/assets/pas_content.png',est_utilisateur=True)
        saisie.value = ''
        # 3. On attend un tout petit peu que le message apparaisse
        await asyncio.sleep(0.05) # Hack technique
        area.scroll_to(percent=1.0)

async def effet_machine_a_ecrire():
    texte_complet = "Bienvenue dans votre application d'agent conversationnel : vous pouvez commencer en entrant un texte dans la zone blanche en bas."
    label_bienvenue.text = "" # On s'assure qu'il est vide au départ
    
    for lettre in texte_complet:
        label_bienvenue.text += lettre
        await asyncio.sleep(0.02) # Vitesse de frappe (40ms par lettre)

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
        with ui.link('Accueil', '/').classes('menu-link'):
            ui.tooltip("Afficher la page chatbot").classes('bulle_info')
        with ui.link('Connexions', '/connections').classes('menu-link'):
            ui.tooltip('Afficher la page de connexion').classes('bulle_info')
        ui.label('HISTORIQUE').classes('text-xs text-brown-8 font-bold my-2')
        
        history = ["Analyse de données", "Correction Bug Python", "Plan de voyage"]

with ui.card().tight().classes('moka-card'):  
    # Zone de Chat
    with ui.scroll_area().classes('w-full h-[500px]') as area:
    # On met une colonne à l'intérieur pour l'espacement des bulles (gap-8)
        chat_container = ui.column().classes('w-full max-w-[800px] mx-auto px-4 py-16 gap-4')
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