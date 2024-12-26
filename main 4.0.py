from PIL import ImageFilter, ImageEnhance
from os import walk
from PIL import Image
from random import randint
from PIL import ImageFont, ImageDraw


def generatePic(text, author="", saveName=""):

    if author == "": author = "Неизвестный автор"

    mer = 0.5

    # Чтение и сохранение слуйчайного изображения в wallPaper

    path = r"./walls"
    filenames = next(walk(path), (None, None, []))[2]  # [] if no file

    try:
        name = filenames[randint(0, len(filenames) - 1)]
        wallPaper = Image.open(path + '/' + name)
    except:
        print("Ошибка при чтении файла")
        quit()

    # Создание текстового поля Canvas и текстового поля для автора ACanvas
    a = 0.6  # width coefficient
    b = 0.6  # height coefficient

    textCanvasSize = (
        round(wallPaper.size[0] * a),  # width
        round(wallPaper.size[1] * b)  # height
    )
    textCanvas = Image.new(
        size=textCanvasSize,
        mode='RGBA',
        color=(0, 0, 0, 0)
    )
    canvasSquare = textCanvasSize[0] * textCanvasSize[1]

    # ACanvas
    a = 0.4  # width coefficient
    b = 0.15  # height coefficient

    ACanvasSize = (
        round(wallPaper.size[0] * a),  # width
        round(wallPaper.size[1] * b)  # height
    )
    ACanvas = Image.new(
        size=ACanvasSize,
        mode='RGBA',
        color=(0, 0, 0, 0)
    )
    ACanvasSquare = ACanvasSize[0] * ACanvasSize[1]

    # Установка фона для mainFont и редактирование шрифта

    textColor = (255, 255, 255)

    fontPath = r"./fonts/calibrii.ttf"
    mainFontSize = 1
    mainFont = ImageFont.truetype(fontPath, mainFontSize)

    authorFontPath = r"./fonts/calibrib.ttf"
    authorFontSize = 1
    authorFont = ImageFont.truetype(authorFontPath, authorFontSize)

    drawText = ImageDraw.Draw(textCanvas)
    drawAuthorText = ImageDraw.Draw(ACanvas)
    mainTextSquare = 0
    authorTextWidth = 0

    # Подгонка текста по площади
    while mainTextSquare < canvasSquare * mer:
        mainFontSize += 1
        mainFont = ImageFont.truetype(fontPath, mainFontSize)
        mainTextSquare = drawText.textbbox(xy=(0, 0), text=text, font=mainFont)[2] * \
                         drawText.textbbox(xy=(0, 0), text=text, font=mainFont)[3]

        while authorTextWidth < ACanvasSize[0]:
            authorFontSize += 1
            authorFont = ImageFont.truetype(authorFontPath, authorFontSize)
            authorTextWidth = drawAuthorText.textbbox(xy=(0, 0), text=author, font=authorFont)[2]


    # Подгонка текста по высоте
    while drawText.textbbox(xy=(0, 0), text=text, font=mainFont)[3] > textCanvasSize[1] * mer:
        mainFontSize -= 1
        mainFont = ImageFont.truetype(fontPath, mainFontSize)
    try:
        mainFont = ImageFont.truetype(fontPath, mainFontSize - 10)
    except: pass

    # Разбиение текста на строки
    text = text.split()
    textLines = []
    maxLines = round(textCanvasSize[1] / drawText.textbbox(xy=(0, 0), text=text[0], font=mainFont)[3])


    currentLine = ""
    staticLine = ""
    for i in range(len(text)):
        currentLine += text[i] + " "
        if drawText.textbbox(xy=(0, 0), text=currentLine, font=mainFont)[2] < textCanvasSize[0]:
            staticLine = currentLine
        else:
            textLines.append(staticLine)
            currentLine = text[i] + " "
            staticLine = currentLine
        if i == len(text) - 1: textLines.append(currentLine)

    # while len(textLines) > maxLines:
    #     textLines = []
    #     mainFontSize -= 1
    #     mainFont = ImageFont.truetype(fontPath, mainFontSize)
    #     w()

    # Размещение строк на Canvas и ACanvas
    y = (textCanvasSize[1] - len(textLines) * drawText.textbbox(xy=(0, 0), text=textLines[0], font=mainFont)[3]) // 2
    dy = drawText.textbbox(xy=(0, 0), text=textLines[0], font=mainFont)[3]
    for line in textLines:
        drawText.text(
            xy=(5 + (textCanvasSize[0] - drawText.textbbox(xy=(0, 0), text=line, font=mainFont)[2]) // 2, y),
            text=line,
            fill=textColor,
            font=mainFont
        )
        y += dy

    drawAuthorText.text(
        xy=((ACanvasSize[0] - drawAuthorText.textbbox(xy=(0, 0), text=author, font=authorFont)[2]) // 2, 2),
        text=author,
        fill=textColor,
        font=authorFont
    )

    # Настройка эффектов для WallPaper

    wallPaper = wallPaper.filter(ImageFilter.BLUR)
    enhancer = ImageEnhance.Brightness(wallPaper)
    wallPaper = enhancer.enhance(0.3)

    # Размещение Canvas на WallPaper
    x = round(wallPaper.size[0] * 0.35)
    y = round(wallPaper.size[1] * 0.25)

    wallPaper.paste(
        im=textCanvas,
        box=(x, y),
        mask=textCanvas
    )

    # Размещение маленькой рамки на WallPaper
    border = Image.open("border.png")
    border = border.resize(
        size=(round(textCanvasSize[0] * 1.09),
              round(textCanvasSize[1] * 1.25)),
        resample=Image.Resampling.NEAREST
    )

    wallPaper.paste(
        im=border,
        box=(round(x * 0.9), round(y * 0.6)),
        mask=border
    )

    # доп. Размещение большой рамки на WallPaper
    border = border.resize(
        size=(round(wallPaper.size[0] ),
              round(wallPaper.size[1] )),
        resample=Image.Resampling.NEAREST
    )
    border = border.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    wallPaper.paste(
        im=border,
        box=(10, 10),
        mask=border
    )

    # Размещение ACanvas на WallPaper
    x = round(x * 1.3)
    y = y + round(textCanvasSize[1] * 0.9)

    wallPaper.paste(
        im=ACanvas,
        box=(x, y),
        mask=ACanvas
    )

    if saveName == "": saveName = name
    # wallPaper.save(rf"./saves/{saveName}.png")
    wallPaper.show()

# from random import randint
#
# for i in range(1):
#     # тут просто для примера всё это расписал
#     text = open("quotes.txt", encoding="utf-8").readlines()
#     text = text[randint(0, len(text) - 1)].split("|")
#
#     author = text[2].replace("\n", "")
#     if author == "": author = "Неизвестный автор"
#
#     text = text[1]
#     generatePic(text, author, f"pic_{i}")
#
text = input("Введи цитату:\n")
author = input("Кто автор:\n")
# while 1:
#     a = input()
#     if a == "###": break
#     text += " " + a

generatePic(text, author)
