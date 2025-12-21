from nicegui import app, ui

# 1. Configuration du dossier d'images
# Assurez-vous que vos fichiers se nomment exactement ainsi dans le dossier /assets
app.add_static_files('/static', './assets')

EMOTIONS = {
    "adore": {"img": "adore.png", "bg": "bg-pink-50", "label": "J'adore ! ❤️"},
    "heureux": {"img": "heureux.png", "bg": "bg-emerald-50", "label": "Heureux 😊"},
    "neutre": {"img": "neutre.png", "bg": "bg-slate-100", "label": "Neutre 😐"},
    "pas_content": {"img": "pas_content.png", "bg": "bg-orange-50", "label": "Pas content 😒"},
    "colere": {"img": "colere.png", "bg": "bg-red-50", "label": "En colère 😡"}
}

# Style pour forcer la transparence du fond de l'avatar au cas où
ui.add_head_html('''
    .ghibli-avatar img { background: transparent !important; object-fit: contain !important; }
''')

with ui.column().classes('w-full items-center p-8 gap-4'):
    ui.label('Testeur de Rendu : Avatars Ghibli').classes('text-2xl font-bold')
    
    with ui.grid(columns=1).classes('w-full max-w-2xl gap-4'):
        for key, info in EMOTIONS.items():
            with ui.card().classes('w-full overflow-hidden'):
                with ui.row().classes('items-center w-full no-wrap'):
                    # Affichage du message de chat
                    ui.chat_message(
                        text=[f"Ceci est le rendu pour l'état : {key}"],
                        name="Assistant Ghibli",
                        avatar=f'/static/{info["img"]}',
                        sent=False
                    ).classes('ghibli-avatar flex-grow').style(f'--q-primary: {info["bg"].replace("bg-", "")}')
                    
                    # Petit badge indicateur de la couleur utilisée
                    ui.badge(info["label"]).classes(f'{info["bg"]} text-black p-2')

ui.run()