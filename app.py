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
        saisie.value = ''
        # 3. On attend un tout petit peu que le message apparaisse
        await asyncio.sleep(0.2) # Hack technique
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
with ui.card().tight().classes('moka-card'):
    # Header
    with ui.row().classes('w-full p-6 justify-between items-center border-b'):
        # Bloc de gauche
        ui.label('Sidora Chatbot').classes('text-2xl font-bold') \
            .style("font-family: 'Caveat', cursive")
        
        # Bloc de droite (regroupé dans une nouvelle row)
        with ui.row().classes('items-center gap-4'):
            ui.switch('Sentiment') \
                .props('color="brown" dense') \
                .bind_value(settings, 'sentiment')
            
            ui.switch('Traduction') \
                .props('color="brown" dense') \
                .bind_value(settings, 'translation')
        

    # Zone de Chat
    with ui.scroll_area().classes('w-full p-16 h-[500px]') as area:
    # On met une colonne à l'intérieur pour l'espacement des bulles (gap-8)
        chat_container = ui.column().classes('w-full p- gap-4')
        label_bienvenue = ui.label('').classes('titre-main text-lg mb-4') \
            .style("font-family: 'Caveat', cursive; min-height: 3em;")

        # On lance l'animation dès que la page est prête
        ui.timer(0.1, effet_machine_a_ecrire, once=True)

    # Input
    with ui.row().classes('w-full p-6 bg-#D9C4BA border-t items-center'):
        with ui.row().classes('w-full items-center bg-stone-50 border rounded-full px-5 py-2'):
            saisie = ui.textarea(placeholder='Veuillez écrire votre message ici...')\
                .props('borderless autogrow')\
                .classes('flex-grow')\
                .style('color: ##FF0000 !important; font-size: 1rem; font-weight: 500;')\
                .on('keydown.enter.prevent', lambda: envoyer_message())
    # Correction ici : on utilise une lambda pour récupérer la valeur au clic
            ui.button(icon='send', on_click=lambda: envoyer_message()) \
                .props('round')\
                .style('background-color: #6e594b !important')
    

ui.run()