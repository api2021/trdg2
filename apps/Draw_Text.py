from PIL import Image, ImageDraw, ImageFont
import glob, os, string,shutil
from fontTools.ttLib import TTFont
import arabic_reshaper

def check_font_support(font_path, text_to_check):
    try:
        font = TTFont(font_path)
        # Check if the font supports the Unicode code points of the Arabic text
        supported = all(ord(char) in font.getBestCmap() for char in text_to_check)
        
        return supported
    except Exception as e:
        print(f"Error while checking font: {e} {font_path[-40:]}")
        return False
    
# texts = []
dict_char = {}

# texts += ["٠١٢٣٤٥٦٧٨٩"]
# texts += ["0123456789"]
letar='أبتثجحخدذرزسشصضطظعغفقكلمنهوي'
# texts += [f"ـ{letar}ـ"]

dict_char['na']={'c':'٠١٢٣٤٥٦٧٨٩'}
dict_char['ne']={'c':'0123456789'}
dict_char['ar']={'c':f"ـ{letar}ـ"}

for i,( ds,df) in enumerate(zip(['ـ',''],['','ـ'])):
    c3=''
    for c in letar:
        c2 = arabic_reshaper.reshape(f'{ds}{c}{df}').replace('ـ','')
        c3+=c2
    # texts += [c3]
    dict_char[f'ar{i}']={'c':c3}

dict_char['en1']={'c':string.ascii_letters[:26]}
dict_char['en2']={'c':string.ascii_letters[26:]}

# texts += [string.ascii_letters[:26],string.ascii_letters[26:]]
# texts += ["«»؟،؛٪"+'=><'+ "!\"#$%&'()*+,-./:;?@[\\]^_`{|}~ "]
# texts += ['≥≤']
# texts += ['✓']

dict_char['sym']={'c':"«»؟،؛٪"+'=><'+ "!\"#$%&'()*+,-./:;?@[\\]^_`{|}~ "}
dict_char['sym_gle']={'c':"≥≤"}
dict_char['sym_c']={'c':"✓"}

# font_dir = r'D:\Projects\AISoftArt\CoVi\OCR\TextRecognitionDataGenerator\trdg\fonts\ar\*'
font_dir = r'D:\Projects\AISoftArt\CoVi\OCR\TextRecognitionDataGenerator\trdg\fonts_combine\**\*'
output_folder = r'D:\Projects\AISoftArt\CoVi\OCR\output_font2'
os.makedirs(output_folder, exist_ok=1)
font0 = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 20)  # Adjust font size as needed
for font_path in glob.glob(font_dir, recursive=1):
    try:
        font = ImageFont.truetype(font_path, 28)  # Adjust font size as needed
    except OSError as e:
        print(f"Error loading font {font_path}: {e}")
        continue

    # Create a new image with a suitable size
    img = Image.new('RGB', (1200, 800), color='black')  # Adjust dimensions as needed
    draw = ImageDraw.Draw(img)

    # Calculate text width and position it centrally
    # text_width, _ = draw.textsize(text, font=font)
    # left, top, right, bottom = font.getbbox(text)
    # text_width, text_height = right - left, bottom - top
    # text_x = (img.width - text_width/2) // 2
    # # text_x = right // 2
    # # text_x = (img.width) // 2
    # # text_x = ((img.width) // 2 ) -text_width//4
    # text_y = img.height // 2

    # Draw the text with black color
    # draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    fontmap = TTFont(font_path)
    # arnum8 = fontm.getBestCmap()[ord('٨')]
    arnum8 = None
    ennum8 = fontmap.getBestCmap()[ord('8')]

    notsupport = []
    support = []
    for i,t in enumerate(fontmap['cmap'].tables):
        try:
            n = t.cmap[ord('٨')]
            # print()
            support+=[n]
        except:
            notsupport+=[i]

    font_name = os.path.basename(font_path)
    font_name = font_path.split('\\')[-2]+f'_{font_name}'
    # u = int(len(text)/3)
    # for i in range(u):
        # draw.text((text_x, text_height*(i+1)), text[u*i:u*(i+1)], font=font, fill=(0, 0, 0))
    for i,(k,chara) in enumerate(dict_char.items()):

            text = chara['c']
            left, top, right, bottom = font.getbbox(text)
            text_width, text_height = right - left, bottom - top
            text_x = (img.width - right) // 2
            text_y = img.height // 2     

            draw.text((text_x, 50*(i+1)), text, font=font, fill='white')

            # left, top, right, bottom = draw.multiline_textbbox((0, 0), text)
            # left, top, right, bottom = draw.textbbox((text_x, 50*(i+1)), text)

            sup = check_font_support(font_path, text)
            chara['sup'] = sup

            draw.text((text_x*1.1+right, 50*(i+1)), f'{sup}', font=font, fill='green' if sup else 'red')

    
    draw.text((text_x*0.5, 50*(i+2)),f'font: {font_name}' , font=font, fill='lightblue')




    # draw.text((10, text_height*20),f'num8:{arnum8},{ennum8} ,sup:{support} notsupport:{notsupport}' , font=font0, fill=(0, 0, 0))

    # Extract font name from path for filename

    output_path = rf"{output_folder}\{font_name}.jpg"  # Adjust output format if needed

    # Save the image with a unique filename
    img.save(output_path)
    print(f"Image saved as: {output_path}")

    if dict_char['sym_c']['sup']:
        destination_path = r'D:\Projects\AISoftArt\CoVi\OCR\output_font_sym_c'
        os.makedirs(destination_path, exist_ok=1)
        shutil.copy(output_path, destination_path)

        destination_path = r'D:\Projects\AISoftArt\CoVi\OCR\TextRecognitionDataGenerator\trdg\fonts_combine\sym_c'
        os.makedirs(destination_path, exist_ok=1)
        try:
            shutil.move(font_path, destination_path)
        except:''

    if dict_char['sym_gle']['sup']:
        destination_path = r'D:\Projects\AISoftArt\CoVi\OCR\output_font_sym_gle'
        os.makedirs(destination_path, exist_ok=1)
        shutil.copy(output_path, destination_path)

        destination_path = r'D:\Projects\AISoftArt\CoVi\OCR\TextRecognitionDataGenerator\trdg\fonts_combine\sym_gle'
        os.makedirs(destination_path, exist_ok=1)
        try:
            shutil.move(font_path, destination_path)

        except:''

    if dict_char['sym']['sup']:
        destination_path = r'D:\Projects\AISoftArt\CoVi\OCR\output_font_sym'
        os.makedirs(destination_path, exist_ok=1)
        shutil.copy(output_path, destination_path)

        destination_path = r'D:\Projects\AISoftArt\CoVi\OCR\TextRecognitionDataGenerator\trdg\fonts_combine\sym'
        os.makedirs(destination_path, exist_ok=1)
        try:
            shutil.move(font_path, destination_path)
        except:''
