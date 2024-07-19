import telebot
from telebot import types
import smtplib
from email.mime.text import MIMEText
from googlesearch import search
import LANGAGES
import os


def rechercher_google(query, num_results=5):
    result_Google = []
    try:
        # Effectuer la recherche
        results = search(query, num_results=num_results)

        # Afficher les résultats
        for i, result in enumerate(results, 1):
            result_Google.append(f"Résultat {i}: {result}")
    except Exception as e:
        return f"Une erreur s'est produite : {e}"

    return result_Google


# Création de l'email


API_TOKEN = os.environ.get("BOT_API_KEY")

bot = telebot.TeleBot(API_TOKEN)

home_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
contact_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
Freelance_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Bienvenue ! Je suis l'assistant personnel de monsieur David Mvoula que Puis faire pour vous ? ",
        reply_markup=home_keyboard,
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if (
        message.text
        == "Contactez le pour un mentoring en développement web (HTML,CSS,JAVASCRIPT) 👨‍💻"
    ):
        bot.send_message(
            message.chat.id,
            "D'accord Il sera ravi de vous accompagner dans votre apprentissage ! 💥🦾",
        )
        bot.send_message(
            message.chat.id,
            "Comment souhaitez vous le contacter ?",
            reply_markup=contact_keyboard,
        )
    elif message.text == "Contactez le pour une Mission Freelance 🚀":
        bot.send_message(
            message.chat.id,
            "Comment souhaitez vous le contacter ?",
            reply_markup=Freelance_keyboard,
        )
    elif (
        message.text
        == "Apprendre un langage de programmation 💁🏽👩🏽‍💻 de façon autonome"
    ):
        bot.send_message(
            message.chat.id,
            "Veuilez un indiquez votre langage de programmation précédé de la commande ##Learn##\n exemple: ##Learn## Python",
        )
    elif message.text == "Par téléphone 📞":
        bot.send_message(message.chat.id, "Son numéro est le +33663851047")
    elif message.text == "Linkedin 📨":
        bot.send_message(
            message.chat.id,
            "Son adresse Linkedin est : https://www.linkedin.com/in/david-mvoula/",
        )
    elif message.text == "Envoyez un mail avec le debrief de la mission 📨":
        bot.send_message(
            message.chat.id,
            "Pour envoyez avec ce chat Bot il est important de commencer votre mail avec ##Mail## \n Exemple: \n ##Mail## \n Bonjour monsieur Mvoula",
        )
    elif message.text.startswith("##Mail##"):
        bot.send_message(message.chat.id, "Votre mail a été reconnu")
        try:
            msg = MIMEText(message.text.replace("##Mail##", ""))
            msg["Subject"] = "Mission Freelance 🚀"
            msg["From"] = os.environ.get("EMAIL_FROM")
            msg["To"] = os.environ.get("EMAIL_TO")
            # Envoi de l'email
            server = smtplib.SMTP(
                "smtp.gmail.com", 587
            )  # Utilisez le serveur SMTP de Gmail avec le port 587
            server.starttls()  # Activez le chiffrement TLS
            server.login(
                os.environ.get("EMAIL_SMTP_USER"), os.environ.get("EMAIL_SMTP_PASSWORD")
            )
            # Envoyer l'email
            server.sendmail(
                os.environ.get("EMAIL_FROM"),
                os.environ.get("EMAIL_TO"),
                msg.as_string(),
            )
            server.quit()
            bot.send_message(message.chat.id, "Email bien Envoyé ✅🫡  ")
        except:
            bot.send_message(
                message.chat.id,
                "Je n'arrive pas à envoyer l'email revenez plus tard 😭😭",
            )
    elif message.text.startswith("##Learn##"):
        langage_to_compare = message.text.replace("##Learn##", "")
        type = ""
        query = ""
        for items in LANGAGES.langages_et_frameworks:
            print(
                langage_to_compare.lower().strip() + " et " + items["langage"].lower()
            )
            if langage_to_compare.lower().strip() == items["langage"].lower():
                type = "Language"
                query = f"Apprendre le {type} " + langage_to_compare.lower().strip()
                result = "\n".join(rechercher_google(query))
                bot.send_message(
                    message.chat.id,
                    f"Le résultat pour la recherce 🔎 {query} :\n " + result,
                )
                break
            elif langage_to_compare.lower().strip() in [
                item.lower() for item in items["frameworks"]
            ]:
                type = "framework"
                query = f"Apprendre le {type} " + langage_to_compare.lower().strip()
                result = "\n".join(rechercher_google(query))
                bot.send_message(
                    message.chat.id,
                    f"Le résultat pour la recherce 🔎 {query} :\n " + result,
                )
                break
        else:
            bot.send_message(
                message.chat.id,
                "Vous vous voulez me piéger c'est raté 🤣🤣 ceci n'est pas un langage de programmation 😭😭😭",
            )

    else:
        bot.send_message(
            message.chat.id, "Je ne comprends pas, veuillez utiliser le clavier."
        )
        bot.send_message(
            message.chat.id,
            " Voici les options disponibles 😀: ",
            reply_markup=home_keyboard,
        )


# HOMEKEYBOARD
button1 = types.KeyboardButton(
    "Contactez le pour un mentoring en développement web (HTML,CSS,JAVASCRIPT) 👨‍💻"
)
button2 = types.KeyboardButton("Contactez le pour une Mission Freelance 🚀")
button3 = types.KeyboardButton(
    "Apprendre un langage de programmation 💁🏽👩🏽‍💻 de façon autonome"
)
home_keyboard.add(button1, button2, button3)

# CONTACT KEYBOARD

button4 = types.KeyboardButton("Par téléphone 📞")
button5 = types.KeyboardButton("Linkedin 📨")
contact_keyboard.add(button4, button5)


# FREELANCE KEYBOARD
button6 = types.KeyboardButton("Envoyez un mail avec le debrief de la mission 📨")

Freelance_keyboard.add(button4, button5, button6)


# Handle '/start' and '/help'


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])


bot.infinity_polling()
