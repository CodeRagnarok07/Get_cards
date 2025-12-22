import os

current_dir = os.path.dirname(__file__)


css_file_data = open(os.path.join(current_dir, 'template', 'style.css'), 'r').read()
back = open(os.path.join(current_dir, 'template', 'back.html'), 'r').read()
front = open(os.path.join(current_dir, 'template', 'front.html'), 'r').read()


TEMPLATE =  {
            'name': 'Gaming Listening',
            'qfmt': front,
            'afmt': back,
            
        }  

CSS = css_file_data

