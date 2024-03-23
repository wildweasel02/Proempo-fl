#Main Views and URL endpoints to frontend of website
from flask import Flask
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_mail import Mail, Message
from email.message import EmailMessage
from flask_login import login_required, current_user
from .models import Feynman, Goal, Journal, Task, FinishedTask, ArchivedTask, Card, Lesson, Pride, Support
from sqlalchemy.orm import aliased
from . import db
import json, os, smtplib
from datetime import date, datetime
import csv
import plotly.graph_objs as go
from datetime import datetime, timedelta
from sqlalchemy import and_, func, text

views = Blueprint('views', __name__)


app = Flask(__name__)


# Get the values of the environment variables
mail_username = os.environ.get('MAIL_USERNAME')
mail_password = os.environ.get('MAIL_PASSWORD')





# Creating the Mail instance
mail = Mail(app)


# Defining the support email address
support_email = "proempohelpdesk@gmail.com" 




@views.route('/')
@login_required
def home():
    qod = generate_quote()
    currentDay = todays_date()
    print(current_user.language)
    if current_user.language == "ro":
        welcome = "Bun venit la ProEmPo, "
        currentDay = "Astăzi este " + today.strftime("%d.%m.%Y")
        openNoisePlayer = "Deschide playerul de zgomot alb"
        journalIncomplete = "Se pare că nu ați finalizat înregistrarea zilnică pentru astăzi."
        clickJournal = "Faceți clic aici pentru a vă completa jurnalul."
        currenttasks = "Sarcini curente:"
        notasks = "Nu aveți sarcini în prezent. Accesați sarcini pentru a face mai multe."
        journalComplete = "Bună treabă, ați completat azi check-in-ul zilnic!"
        dueReminder = "Datorită:"
    else:
        welcome = "Welcome to ProEmPo, "
        currentDay = currentDay
        openNoisePlayer = "Open Noise Player"
        journalIncomplete = "It looks like you haven't completed your daily check-in for today."
        clickJournal = "Click here to fill out your journal."
        currenttasks = "Current Tasks:"
        notasks = "You have no tasks currently. Go to tasks to make more."
        journalComplete = "Good Job, you filled out your daily check-in today!"
        dueReminder = "Due:"
    entry_for_today = Journal.query.filter(Journal.date == today, Journal.user_id == current_user.id).first()
    tasks = Task.query.filter(Task.user_id == current_user.id).order_by(text(current_user.defaultsort))

    return render_template("home.html", tasks=tasks, notasks=notasks, currenttasks=currenttasks, user=current_user, qod=qod, currentDay=currentDay, welcome=welcome,
                            openNoisePlayer=openNoisePlayer, entry_for_today=entry_for_today, journalIncomplete=journalIncomplete, 
                            dueReminder=dueReminder, clickJournal=clickJournal, journalComplete=journalComplete)

today = date.today()

def todays_date():
    day_str = today.strftime('%d')
    day_int = int(day_str)
    
    
    if day_int < 10:
        day = (today.strftime('%d')).lstrip('0')
    else:
        day = (today.strftime('%d'))
    
    if (day_int % 10 == 1):
        day = day + 'st'
    elif (day_int % 10 == 2):
        day = day + 'nd'
    elif (day_int % 10 == 3):
        day = day + 'rd'
    else:
        day = day + 'th'

    currentDay = today.strftime('%A, %B ' + day + ', %Y')

    return currentDay
def generate_quote():
    csv_file_path = os.path.join(app.root_path, 'static', 'list.csv')
    with open(csv_file_path, 'r') as f:

        reader = csv.reader(f, delimiter=',')
        epoch = datetime(2023, 10, 1)
        today = datetime.now()
        currentDay = (today - epoch).days
        num_lines = sum(1 for _ in reader)
        index = currentDay % num_lines
        f.seek(0)
        

        for i, row in enumerate(reader):
            if i == index:
                if(row[0] == "") :
                    row[0] = "Unknown Author"
                qod = (row[1], row[0]) 
                break
        else:
            qod = "Error: Quote not found."

    return qod

@app.route('/toggle_white_noise', methods=['POST'])
@login_required
def toggle_white_noise():
    print("Form submitted")
    # Handle the white noise play/pause action based on the form submission (your implementation)
    return redirect(url_for('views.home'))  # Redirect back to the home page after handling the action






@views.route('/help')
@login_required
def help():
    print(current_user.language)
    if current_user.language == "ro":
        cSelfWork = "Concentrare"
        pomodoroDescription = "Încercați tehnica Pomodoro pentru a vă crește productivitatea."
        flashcards = "Carduri Flash"
        flashcardsDescription = "Folosiți carduri pentru a memora informații în mod eficient."
        create = "Crează"
        view = "Arată"
        feynmanDescription = "Stăpânește subiecte complexe explicând-o unei entități mai mici în termeni simpli."
        iSelfWork = "Munca De Sine"
        accomplishments = "Realizări"
        prideDescription = "Lucrează la sufletul tau interior enumerând lucruri care te fac să te simți mândru de tine."
        begin = "Începe"
        goals = "Obiective"
        goalsDescription = "Enumerați-vă obiectivele pe termen lung pentru a vă ajuta să rămâneți concentrat pe ceea ce este important pentru dumneavoastră."
        meditation = "Meditaţie"
        meditationDescription = "Găsiți pace și reduceți stresul prin respirație ghidată."
        youngEdition = "Ediția Tânără"
        collegeEdition = "Ediția Pentru Colegiu"
    else:
        cSelfWork = "Concentration Self-Work"
        pomodoroDescription = "Try the Pomodoro Technique to boost your productivity."
        flashcards = "Flashcards"
        flashcardsDescription = "Use flashcards to memorize information effectively."
        create = "Create"
        view = "View"
        feynmanDescription = "Master complex subjects by explaining it to a smaller entity in simple terms."
        iSelfWork = "Inner Self-Work"
        accomplishments = "Accomplishments"
        prideDescription = "Work on your inner self by listing things that make you feel proud of yourself."
        begin = "Begin"
        goals = "Goals"
        goalsDescription = "List your long term goals to help you remain focused on what is important to you."
        meditation = "Meditation"
        meditationDescription = "Find peace and reduce stress through paced breathing."
        youngEdition = "Young Edition"
        collegeEdition = "College Edition"
    return render_template("help.html", user=current_user, cSelfWork=cSelfWork, pomodoroDescription=pomodoroDescription, 
                           flashcards=flashcards, flashcardsDescription=flashcardsDescription, create=create, view=view, 
                           feynmanDescription=feynmanDescription, iSelfWork=iSelfWork, accomplishments=accomplishments, 
                           prideDescription=prideDescription, begin=begin, goals=goals, goalsDescription=goalsDescription, 
                           meditation=meditation, meditationDescription=meditationDescription, youngEdition=youngEdition, collegeEdition=collegeEdition)

@views.route('/feynman')
@login_required
def feynman():
    latest_entry = Feynman.query.filter_by(user_id=current_user.id).order_by(Feynman.id.desc()).first()

    # Replacing newline characters with <br> tags for proper display in HTML
    if latest_entry:
        latest_entry.description = latest_entry.description.replace('\n', '<br>')


    if current_user.language == "ro":
        title="Metoda Feynman"
        question="Cum încep?"
        writeTitle= "Scrie titlul aici"
        writeDescription="Scrie descrierea aici"
        startNew = "începe Nou"
        RememberThoughts="Salvează-mi gândurile pentru data viitoare"
        explanation1="Metoda Feynman are 4 pași simpli:"
        explanation2="După ce ați studiat subiectul, începeți să îl scrieți într-un limbaj simplu. Gândiți-vă la asta ca la explicarea subiectului ales unui copil mic. Dacă există lacune în înțelegerea dvs., completați-le și încercați din nou. Ideea principală este că, dacă nu reușiți să-l explicați simplu, nu îl înțelegeți suficient de bine și aveți nevoie de mai multă practică."
        explanation3="Acum, închideți fereastra asta și începeți."
    else:
        title="Feynman Method"
        question="How do I begin?"
        writeTitle="Write topic here"
        writeDescription="Write description here"
        startNew = "Start New"
        RememberThoughts ="Remember my thoughts for next time"
        explanation1="The Feynman Method has 4 easy steps"
        explanation2="After studying your topic, begin writing it down in simple language. Think of it as explaining your choosen topic to a toddler. If there are gaps in your understanding, fill them in and try again. The core point is that if you are unable to explain it simply, you don't understand it well enough and need more practice."
        explanation3="Now, close this popup and begin."

    return render_template("feynman.html", user=current_user, latest_entry=latest_entry, 
                           title=title, question=question, writeTitle=writeTitle, writeDescription=writeDescription, startNew=startNew,
                           RememberThoughts=RememberThoughts, explanation1=explanation1, explanation2=explanation2, explanation3=explanation3)

@views.route('/start-new-entry', methods=['POST'])
@login_required
def start_new_entry():
    new_feynman_entry = Feynman(user_id=current_user.id, title='', description='')
    db.session.add(new_feynman_entry)
    db.session.commit()

    return redirect(url_for('views.feynman'))


@views.route('/save-data', methods=['POST'])
@login_required
def save_data():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    # Save the data to the database for the current user
    new_feynman_entry = Feynman(
        user_id=current_user.id,
        title=title,
        description=description
    )

    db.session.add(new_feynman_entry)
    db.session.commit()

    return jsonify({'message': 'Data saved successfully'})

@views.route('/pomodoro')
@login_required
def pomodoro():
    task_id = request.args.get('taskId')
    task_data = request.args.get('taskData')
    uncompleted_tasks = Task.query.filter_by(user_id=current_user.id).all()

    if current_user.language == "ro":
        title="Ceas Pomodoro"
        start="Începe"
        pause="Pauză"
        reset="Resetă"
        workTime="Timp de muncit (min)"
        shortBreak="Pauză mică (min)"
        longBreak="Pauză lungă (min)"
        task = "În această sesiune voi lucra la:"
        question="Ce este Pomodoro?"
        explanation1="Tehnica Pomodoro este o metodă de gestionare a timpului care folosește un cronometru pentru a descompune munca în intervale."
        explanation2="5 pași simpli:"
        explanation3="1. Decideți asupra sarcinii pe care trebuie să o faceți"
        explanation4="2. Setați timpul de lucru la 25 de minute (reglabil)"
        explanation5="3. Lucrați la sarcina stabilită până când sună cronometrul"
        explanation6="4. Luați o scurtă pauză de 5 minute (reglabilă)"
        explanation7="5. După 4 sesiuni, luați o pauză mai lungă."
    else: 
        title="Pomodoro Timer"
        start="Start"
        pause="Pause"
        reset="Reset"
        workTime="Work Time (min)"
        shortBreak="Short Break (min)"
        longBreak="Long Break (min)"
        question="What is Pomodoro?"
        explanation1="The Pomodoro Technique is a time management method that uses a timer to break down work in intervals."
        explanation2="5 easy steps:"
        explanation3="1. Decide on the task that you need to do"
        explanation4="2. Set the work time to 25 minutes (adjustable)"
        explanation5="3. Work on the set task until the timer rings"
        explanation6="4. Take a short 5 minute break (adjustable)"
        explanation7="5. After 4 cycles, take a longer break."

    return render_template('pomodoro.html', task_id=task_id, task_data=task_data, user=current_user, uncompleted_tasks=uncompleted_tasks, 
                           title=title, start=start, pause=pause, reset=reset, workTime=workTime, shortBreak=shortBreak, longBreak=longBreak, 
                           question=question, explanation1=explanation1, explanation2=explanation2, explanation3=explanation3, explanation4=explanation4, 
                           explanation5=explanation5, explanation6=explanation6, explanation7=explanation7)


@views.route('/FAQ')
@login_required
def faq():
    if current_user.language == "ro":
        accordion_items = [
    {
        "id": "section1",
        "title": "Începerea",
        "content": "",
        "nested_items": [
            {"id": "nested1", "title": "Există un tutorial sau un proces de inițiere care să mă ajute să navighez în aplicație pentru prima dată?", "content": "Ne pare rău, site-ul web nu oferă niciun tutorial sau nu oferă niciun proces."},
            {"id": "nested2", "title": "Care este modelul de preț pentru site-ul dvs.? Există versiuni gratuite sau de încercare disponibile?", "content": "Acest site este gratuit, nu există un model de preț sau versiuni de încercare."},
            {"id": "nested3", "title": "Ce este tehnica pomodoro? Cum o pot utiliza pe site?", "content": "Tehnica pomodoro este o metodă de gestionare a timpului bazată pe sesiuni de lucru concentrate de 25 de minute întrerupte de pauze de cinci minute. Puteți utiliza această tehnică în pagina de Ajutor personal."},
            {"id": "nested4", "title": "Ce este tehnica Feynman? Cum o pot utiliza pe site?", "content": "Tehnica Feynman este un proces în patru pași pentru înțelegerea oricărui subiect. Ea respinge reținerea automată în favoarea înțelegerii autentice obținute prin selecție, cercetare, scriere, expunere și rafinare. Puteți găsi această tehnică în pagina de Ajutor personal."},
            {"id": "nested5", "title": "Ce este zgomotul alb? Cum mă poate ajuta zgomotul alb în timp ce utilizez acest site?", "content": "Zgomotul alb este un sunet constant și uniform care conține putere egală la toate frecvențele auzibile. Vă poate ajuta prin mascarea zgomotului de fundal, îmbunătățirea concentrării și a atenției și crearea unui mediu sonor constant."},
            {"id": "nested6", "title": "Unde pot să merg pentru a lua legătura cu suportul dacă nu sunt disponibile problemele listate pe pagină?", "content": "Puteți vizita pagina de Suport din bara de navigație și să vă listați problemele acolo."}
        ],
    },
    {
        "id": "section2",
        "title": "Sănătatea Mintală",
        "content": "",
        "nested_items": [
            {"id": "nested8", "title": "Care este relația dintre sănătatea mintală și productivitate?", "content": "Starea sănătății mintale și nivelul de productivitate au o relație foarte strânsă, însă mulți oameni aleg să ignore această relație. Sănătatea mintală constă în multe aspecte, cum ar fi stresul, anxietatea și depresia. De obicei, o persoană care se confruntă cu aceste provocări va avea niveluri mai scăzute de implicare, creativitate și rezolvare a problemelor. Proempo încearcă să mențină o relație pozitivă între aceste două aspecte ale vieții."},
            {"id": "nested9", "title": "Cum mă va ajuta Proempo să gestionez stresul și anxietatea?", "content": "Ca studenți, noi, la Proempo, avem multă empatie față de oamenii care luptă să-și controleze gândurile și sunt foarte stresați din cauza termenelor limită. Organizarea vieții tale este un mod excelent de a începe să faci față stresului și/sau anxietății. Păstrând toate activitățile, temele școlare sau pur și simplu notele și amintirile generale într-un loc central ușor accesibil. Acest lucru va arăta cât timp ai pentru a face aceste sarcini. Te vei simți în siguranță văzând că ai completat sarcinile. Proempo oferă și o secțiune de jurnalizare pentru a ajuta cu anxietatea trăită în viața ta de zi cu zi."},
            {"id": "nested10", "title": "Care este scopul jurnalizării?", "content": "Jurnalizarea este o activitate excelentă pentru a te ajuta pe tine însuți. În timpul jurnalizării, nu există factori externi de care să-ți faci griji, în afara lui „Eu, eu și eu”. Acesta este un spațiu sigur în care poți elibera toate gândurile și sentimentele acumulate pe o pagină. Pe măsură ce trece timpul, vei avea multe jurnale care îți vor arăta cum te-ai simțit într-o zi anume și motivul pentru care acea zi a avut acel rezultat. Privind înapoi la aceste jurnale, vei vedea cât de mult te-ai dezvoltat ca persoană și vei învăța din trecutul tău."},
            {"id": "nested11", "title": "Ce este epuizarea și ce trebuie să fac dacă o experimentez?", "content": "Epuizarea este o stare de oboseală fizică și/sau emoțională care poate afecta identitatea cuiva și sentimentul de a fi realizat. Pașii pentru a reduce epuizarea încep cu căutarea de sprijin din partea membrilor familiei sau colegilor pentru a vă ajuta să colaborați și să faceți față a ceea ce simțiți. Puteți să încercați să vă dedicați timp unei activități sau hobby pe care îl apreciați și care vă relaxează sau chiar să faceți exerciții. „Leacul” pentru epuizare constă în a lua o pauză de la muncă sau școală sau de la alte factori care ar putea cauza această stare."},
            {"id": "nested12", "title": "Unde pot să merg pentru a cere ajutor?", "content": "Dacă aveți nevoie de ajutor serios sau de suport dincolo de serviciile noastre, iată câteva resurse pe care le puteți verifica: Linia de viață pentru suicid și criză: 988, Terapie."}
        ],
    },
    {
        "id": "section3",
        "title": "Productivitate",
        "content": "",
        "nested_items": [
            {"id": "nested13", "title": "Ce funcționalități oferă site-ul pentru a îmbunătăți productivitatea?", "content": "Funcționalitățile oferite pe site sunt metoda pomodoro și tehnica Feynman, ambele fiind disponibile în pagina de Ajutor personal."},
            {"id": "nested14", "title": "Puteți oferi sfaturi pentru stabilirea și atingerea obiectivelor de productivitate?", "content": "Sfaturile noastre pentru utilizarea acestui site în stabilirea și atingerea obiectivelor includ crearea de sarcini, utilizarea metodei pomodoro, crearea de carduri cu întrebări și realizarea de pauze pentru a preveni epuizarea."},
            {"id": "nested15", "title": "Cum joacă gestionarea timpului un rol în productivitate? Poate site-ul dvs. să ajute în acest sens?", "content": "Gestionarea timpului joacă un rol crucial în productivitate, ajutând persoanele să-și prioritizeze sarcinile, să aloce timp eficient și să minimizeze distragerile. O gestionare eficientă a timpului permite o mai bună organizare și le permite persoanelor să realizeze mai mult în mai puțin timp, ceea ce duce la o productivitate mai mare. Site-ul nostru poate oferi utilizatorilor crearea unei sarcini în pagina de sarcini, utilizarea metodei pomodoro pentru a seta un cronometru, împreună cu finalizarea sarcinilor create din pagina de sarcini, crearea de carduri cu întrebări în pagina de Ajutor personal, etc. Vă rugăm să verificați pagina de Ajutor personal dacă doriți să vă îmbunătățiți productivitatea."},
            {"id": "nested16", "title": "Care sunt câteva strategii pentru a învinge procrastinarea și a menține concentrarea?", "content": "Site-ul nostru poate lista câteva strategii. Descompuneți sarcinile în pași mai mici. Stabiliți obiective specifice și realizabile. Utilizați un cronometru pentru muncă concentrată, precum metoda pomodoro. Minimizați distragerile cu ajutorul player-ului nostru de zgomot alb încorporat. Răsfățați-vă pentru finalizarea sarcinilor. Creați un spațiu de lucru dedicat. Prioritizați sarcinile în funcție de importanță și urgență."},
            {"id": "nested17", "title": "Cum pot să prioritizez eficient sarcinile și proiectele pentru a-ți optimiza productivitatea?", "content": "Puteți prioritiza sarcinile utilizând steaua ca o modalitate de a vă favoriza sarcinile, personalizarea suplimentară este disponibilă în setări. În ceea ce privește proiectele, deocamdată nu oferim nimic pentru prioritizarea proiectelor pe site."},
            {"id": "nested18", "title": "Cum pot să urmăresc progresul și să măsurăm câștigurile de productivitate folosind site-ul?", "content": "Puteți urmări progresul pe site cu ajutorul graficelor și diagramele furnizate pentru a măsura progresul dvs. actual de productivitate."}
        ],
    },
]
        FAQtitle = "Întrebări frecvente"
        subtitle = "Dacă aveți alte întrebări, vă rugăm să consultați celelalte secțiuni de mai jos."
    else:
        accordion_items = [
            {
                "id": "section1",
                "title": "Getting Started",
                "content": "",
                "nested_items": [
                    {"id": "nested1", "title": "Is there a tutorial or onboarding process to help me navigate the application for the first time?", "content": "Sorry, the website doesn't provide any tutorial or offer any process."},
                    {"id": "nested2", "title": "What is the pricing model for your website? Are there any free or trial versions available?", "content": "This website is free, there is no pricing model nor any trial versions."},
                    {"id": "nested3", "title": "What is the pomodoro technique? How can I use it on the website?", "content": "The pomodoro technique is a time management method based on 25-minute stretches of focused work broken by five-minute breaks. You can use the technique located in the Self-Help page."},
                    {"id": "nested4", "title": "What is the feynman technique? How can I use it on the website?", "content": "The feynman technique is a four-step process for understanding any topic. It rejects automated recall in favor of true comprehension gained through selection, research, writing, explaining, and refining. You can find it located in the self-help page."},
                    {"id": "nested5", "title": "What is white noise? How can white noise help me while using this website?", "content": "White noise is a consistent and uniform sound that contains equal power across all audible frequencies. It can help you by masking background noise, improving focus and concentration, and having a consistent sound environment."},
                    {"id": "nested6", "title": "Where can I go to contact support if any of the issues listed in the page aren't available?", "content": "You can visit the Support page in the navigation bar and list your issues there."}
                ],
            },
            {
                "id": "section2",
                "title": "Mental Health",
                "content": "",
                "nested_items": [
                    {"id": "nested8", "title": "What is the relationship between mental health and productivity?", "content": "The state of your mental health and how productive you are, have a very interconnected relationship but, many people choose to ignore this relationship. Mental health consists of many things such as stress, anxiety, and depression. Typically, someone who has any of these challenges will experience lower levels of engagement, creativity and problem solving. Proempo looks keep a positive relationship between these two factors of life."},
                    {"id": "nested9", "title": "How will Proempo help me manage my stress and anxiety?", "content": "As students, here at Proempo, we have a lot of empathy towards people struggling to control their thoughts and are very stressed about deadlines. Organizing your life is a great way to get started with handling your stress and/or anxiety. By keeping all your activities, schoolwork, or just general notes and reminders in one centrally located place that is easily accessible. Having this will layout how much time you have to do these tasks. You will be at ease seeing that your tasks are completed. Proempo also offers a journaling section to help with anxiety experienced in your everyday life."},
                    {"id": "nested10", "title": "What is the point of journaling?", "content": "Journalling is a great activity to help yourself. While journaling there are no outside factors to worry about except “Me, myself and I”. This is a safe space where you can heave all your pent-up thoughts and feelings onto a page. As time goes on you will have many journals telling you how you felt during a particular day and the reason that day followed that outcome. Looking back at these journals will show you how much you have developed as a person and learn from your past self."},
                    {"id": "nested11", "title": "What is burnout and what to do if I experience it?", "content": "Burnout is a state of physical and/or emotional exhaustion that can come to effect someone’s identity and sense of feeling accomplished. Steps to help reduce burnout starts with seeking support from family members or colleagues to help you collaborate and cope with what you are feeling. You could go ahead and try an activity or hobby you really enjoy that gets you relaxed or even exercise. The “cure” to burnout is taking a break from either work or school or other factors that might be causing this."},
                    {"id": "nested12", "title": "Where can I go to seek support?", "content": "If in need of serious help or support beyond our services, here are some resources to look into: Suicide and Crisis lifeline: 988, Therapy."}
                
                ],
            },
            {
                "id": "section3",
                "title": "Productivity",
                "content": "",
                "nested_items": [
                    {"id": "nested13", "title": "What features does the website offer to enhance productivity?", "content": "The features offered in the website are the pomodoro method, feynman technique, which are both located in the self-help page."},
                    {"id": "nested14", "title": "Can you provide tips for settings and achieving productivity goals?", "content": "Our tips to utilizing this website for setting and achieving goals are creating tasks, using the pomodoro method, creating flashcards, and taking a break to prevent burnout."},
                    {"id": "nested15", "title": "How does time management play a role in productivity? Can your website assist with this?", "content": "Time management plays a crucial role in productivity by helping individuals prioritize tasks, allocate time efficiently, and minimize distractions. Effective time management enables better organization and allows individuals to accomplish more in less time, leading to increased productivity. Our website can offer users with creating a task withing the tasks page, using the pomodoro method to set a timer along with completing the tasks created from the task page, creating flashcards in the self-help page, etc. Please check the self-help page if you want to enhance your productivity."},
                    {"id": "nested16", "title": "What are some strategies for overcoming procrastination and maintaining focus?", "content": "Our website can list some strategies. Break tasks into smaller steps. Set specific, achievable goals. Use a timer for focused work like the pomodoro method. Minimize distractions with our built-in white noise player. Reward yourself for completing tasks. Create a dedicated workspace. Prioritize tasks based on importance and urgency."},
                    {"id": "nested17", "title": "how can I effectively priortize tasks and projects to optimize my productivity?", "content": "You can priortize tasks by using the star as a way to favorite tasks, further customization is available in the settings. As for projects, we don't offer anything to priortize projects on the website for now."},
                    {"id": "nested18", "title": "How can I track my progress and measure my productivity gains using the website?", "content": "You can track progress in the website with the provided graphs and charts to measure your current productivity progress."},
                ],
            },
        
        ]
        FAQtitle = "Frequently Asked Questions"
        subtitle = "If you have other questions, please check out the other sections below."
    return render_template("FAQ.html", user=current_user, accordion_items=accordion_items, FAQtitle=FAQtitle, subtitle=subtitle)



@views.route('/bearMeditation')
@login_required
def bearMeditation():
    return render_template("bearMeditation.html", user=current_user)

@views.route('/regularMeditation')
@login_required
def regularMeditation():
    return render_template("regularMeditation.html", user=current_user)

@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if current_user.language == "ro":
        taskTitle = "Sarcini"
        dueDate = "Data Scadenței: (Opțional)"
        dueTime = "Timp Cuvenit: (Opțional)"
        taskEnter = "Sarcină:"
        taskButton = "Adăugați o Sarcină"
        congrats1 = "Felicitări! Nu ai sarcini!"
        congrats2 = "Faceți o nouă sarcină mai sus."
        taskDueDate = "Data Scadenței:"
        at = "la"
        archiveTaskButton = "Sarcini Arhivate"
        sortBy = "Filtrează după"
        oldToNew = "De la cel mai vechi la cel mai nou"
        newToOld = "De la cel mai nou la cel mai vechi"
        sortDueDate = "Data Scadenței"
        alphabetically = "Alfabetic"
        sortDefault = "(Mod Implicit)"
    else:
        taskTitle = "Tasks"
        dueDate = "Due Date: (Optional)"
        dueTime = "Due Time: (Optional)"
        taskEnter = "Task:"
        taskButton = "Add Task"
        congrats1 = "Congratulations! You have no tasks!"
        congrats2 = "Make a new task above."
        taskDueDate = "Due Date:"
        at = "at"
        archiveTaskButton = "Archived Tasks"
        sortBy = "Sort by"
        oldToNew = "Oldest to Newest"
        newToOld = "Newest to Oldest"
        sortDueDate = "Due Date"
        alphabetically = "Alphabetically"
        sortDefault = "(Default)"

    if request.method == 'POST':
        task_data = request.form.get('task')  # Gets the task from the HTML
        due_date_str = request.form.get('dueDate')  # Gets the due date string
        due_time_str = request.form.get('dueTime')  # Gets due time

        if len(task_data) < 1:
            flash('You must enter a task!', category='error')
        elif due_time_str and not due_date_str:
            flash('You cannot have a due time without choosing a due date!', category='error')
        else:
            due_date = None  # Default to None if no due date is provided
            due_time = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

            if due_time_str:
                due_time = datetime.strptime(due_time_str, '%H:%M').time()

            new_task = Task(
                data=task_data,
                due_date=due_date,
                due_time=due_time,
                user_id=current_user.id
            )

            db.session.add(new_task)  # Add the task to the database
            db.session.commit()
            flash('Task added!', category='success')

    selected_sort = request.args.get('sort_method', 'default')

    user_id = current_user.id

    if selected_sort == 'due_date':
        tasks = Task.query.filter(Task.user_id == user_id).order_by(Task.due_date, Task.due_time)
    elif selected_sort == 'data':
        tasks = Task.query.filter(Task.user_id == user_id).order_by(func.lower(Task.data))
    elif selected_sort == 'newest':
        tasks = Task.query.filter(Task.user_id == user_id).order_by(Task.date.desc())
    elif selected_sort == 'oldest':
        tasks = Task.query.filter(Task.user_id == user_id).order_by(Task.date)
    else:
        tasks = Task.query.filter(Task.user_id == user_id).order_by(text(current_user.defaultsort))


    return render_template('tasks.html', user=current_user, dueDate=dueDate, dueTime=dueTime, taskTitle=taskTitle, 
                           tasks=tasks, taskEnter=taskEnter, taskButton=taskButton, congrats1=congrats1, congrats2=congrats2, 
                           taskDueDate=taskDueDate, at=at, archiveTaskButton=archiveTaskButton, sortBy=sortBy, selected_sort=selected_sort,
                           oldToNew=oldToNew, newToOld=newToOld, sortDueDate=sortDueDate, alphabetically=alphabetically, sortDefault=sortDefault)


@views.route('/archivedtasks')
@login_required
def archivedtasks():
    if current_user.language == "ro":
        noArchivedTasks = "Nimic aici..."
        archiveWarning = "Sigur doriți să ștergeți definitiv această sarcină? Odată ce o sarcină este ștearsă, aceasta nu va mai fi luată în considerare în statisticile și graficele dvs. Vă recomandăm să nu ștergeți sarcini decât dacă doriți cu adevărat."
    else:
        noArchivedTasks = "Nothing Here..."
        archiveWarning = "Are you sure you want to permanently delete this task? Once a task is deleted it will no longer be factored into your statistics and charts. We recommend not deleting tasks unless you really want to."
    archivedtasks = ArchivedTask.query.filter_by(user_id=current_user.id).order_by(ArchivedTask.date).all()
    return render_template('archivedtasks.html', archivedtasks=archivedtasks, noArchivedTasks=noArchivedTasks, archiveWarning=archiveWarning, user=current_user)
    


@views.route('/reports')
@login_required
def reports():
    if current_user.language == "ro":
        reportsTitle = "Rapoarte"

    else:
        reportsTitle = "Reports"
    #code for the first graph on page
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6) 
    finished_tasks_data = (
        db.session.query(
            func.strftime('%Y-%m-%d', FinishedTask.date).label('date'),
            func.count(FinishedTask.id).label('finished_count')
        )
        .filter(FinishedTask.user_id == current_user.id)
        .filter(FinishedTask.date >= start_date)
        .filter(FinishedTask.date <= end_date)
        .group_by(func.strftime('%Y-%m-%d', FinishedTask.date))
        .all()
    )
    archived_tasks_data = (
        db.session.query(
            func.strftime('%Y-%m-%d', ArchivedTask.date).label('date'),
            func.count(ArchivedTask.id).label('finished_count')
        )
        .filter(ArchivedTask.user_id == current_user.id)
        .filter(ArchivedTask.date >= start_date)
        .filter(ArchivedTask.date <= end_date)
        .group_by(func.strftime('%Y-%m-%d', ArchivedTask.date))
        .all()
    )
    data_dict = {}
    current_day = start_date
    while current_day <= end_date:
        formatted_date = current_day.strftime('%Y-%m-%d')
        data_dict[formatted_date] = 0  # Initialize all days with zero completed tasks
        current_day += timedelta(days=1)

    for row in finished_tasks_data:
        date_str = row.date
        data_dict[date_str] = row.finished_count

    for row in archived_tasks_data:
        date_str = row.date
        data_dict[date_str] += row.finished_count


    finished_tasks_list = [{'date': date, 'finished_count': count} for date, count in data_dict.items()]
    finished_tasks_json = json.dumps(finished_tasks_list)

    # Query to find the most popular day-rating
    most_popular_day_rating = (
        db.session.query(Journal.day_rating, func.count().label('count'))
        .filter(Journal.user_id == current_user.id)
        .group_by(Journal.day_rating)
        .order_by(func.count().desc())
        .limit(1)
        .first()
    )

    most_popular_rating = most_popular_day_rating[0] if most_popular_day_rating else "No data available"
    # !!!!! need to handle what happens when there is a tie




    # Code for the second visualization
    goals_count = Goal.query.filter(
        and_(Goal.user_id == current_user.id, Goal.status == "C")
    ).count()

    latest_completed_goals = Goal.query.filter(
        and_(Goal.user_id == current_user.id, Goal.status == "C")
    ).order_by(Goal.date.desc()).limit(3).all()

    day_ratings = Journal.query.filter_by(user_id=current_user.id).with_entities(Journal.date, Journal.day_rating).all()

    # Map day ratings to numerical values
    converted_ratings = {'horrible': 1, 'bad': 2, 'good': 3, 'excellent': 4}
    day_rating_data = [{'date': str(date), 'rating': converted_ratings.get(rating.lower(), 0)} for date, rating in day_ratings]

    day_rating_json = json.dumps(day_rating_data)
    print(day_rating_json)



    if current_user.language == "ro":
        chart1Title="Sarcinile pe care le-am finalizat în această săptămână"
        goalsAchieved="Obiective Realizate"
        latestCompletedGoals="Ultimele obiective îndeplinite"
        mostFrequentDayRating="Evaluarea mea cea mai frecventă de zi"
        myHistory="Istoricul evaluării zilei mele"
        noDayRatings="Se pare că nu ați înregistrat nicio evaluare zilnică. Vă rugăm să adăugați aceste date pentru a vă putea genera raportul."
        no_goals_message="Se pare că nu ți-ai stabilit niciun obiectiv."
        dayHistory = "Istoricul evaluării zilei mele"
    else:
        chart1Title="Amount of tasks I completed this week"
        goalsAchieved="Goals Achieved"
        latestCompletedGoals = "Latest Completed Goals"
        mostFrequentDayRating="My most frequent day rating"
        myHistory="My Day Rating History"
        noDayRatings="It appears that you have not logged any day ratings. Please add this data so that we can generate your report."
        no_goals_message="It appears as if you have not set any goals."
        dayHistory = "My Day Rating History"
    if goals_count > 0:
        return render_template("reports.html", user=current_user, reportsTitle=reportsTitle, finished_tasks=finished_tasks_json, goals_count=goals_count, latest_completed_goals=latest_completed_goals, most_popular_rating=most_popular_rating, day_rating_json=day_rating_json, 
                               chart1Title=chart1Title, goalsAchieved=goalsAchieved, latestCompletedGoals=latestCompletedGoals,
                               mostFrequentDayRating=mostFrequentDayRating, myHistory=myHistory, noDayRatings=noDayRatings, dayHistory=dayHistory)
    else:
        return render_template("reports.html", user=current_user, reportsTitle=reportsTitle, finished_tasks=finished_tasks_json, goals_count=goals_count, no_goals_message=no_goals_message, most_popular_rating=most_popular_rating, day_rating_json=day_rating_json, 
                               chart1Title=chart1Title, goalsAchieved=goalsAchieved, latestCompletedGoals=latestCompletedGoals,
                               mostFrequentDayRating=mostFrequentDayRating, myHistory=myHistory, noDayRatings=noDayRatings, dayHistory=dayHistory)


@views.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    selected_entry = None  #Initialize selected_entry to None
    if current_user.language == "ro":
        journalTitle = "Verificare Zilnică"
        journalSelect = "Selectați o intrare anterioară:"
        journalChoose = "Selectați o intrare"
        journalButton = "Aplică"
        journalDate = "Data:"
        dearJournal = "Draga Jurnalule,"
        journalContent = "Astăzi, mi-am petrecut ziua gândindu-mă la..."
        gratefulContent = "3 lucruri pentru care sunt recunoscător astăzi sunt:"
        dayTitle = "Ziua mea a fost..."
        rating_excellent = "Excelent"
        rating_good = "Bun"
        rating_bad = "Rău"
        rating_horrible = "Oribil"
        saveJournal = "Salvați"
        journalFooter = "Ceea ce este în mintea ta?"
    else:
        journalTitle = "Daily Check-In"
        journalSelect = "Select a previous entry:"
        journalChoose = "Select an entry"
        journalButton = "Go"
        journalDate = "Date:"
        dearJournal = "Dear Journal,"
        journalContent = "Today, I spent my day thinking about..."
        gratefulContent = "3 things I am grateful for today are:"
        dayTitle = "My day was..."
        rating_excellent = "Excellent"
        rating_good = "Good"
        rating_bad = "Bad"
        rating_horrible = "Horrible"
        saveJournal = "Save Entry"
        journalFooter = "What is on your mind?"
    today = datetime.now().date()
    entry_for_today = Journal.query.filter(Journal.date == today, Journal.user_id == current_user.id).first()
    if entry_for_today:
        selected_entry = entry_for_today


    if request.method == 'POST':
        if is_entry_exists_for_today():
            flash('Entry already exists for today. Cannot check-in again today.', category='error')
        else:

            #Handle form submission
            date = datetime.now().date()
            dear_journal_content = request.form.get('dear_journal_content')
            grateful_contents = [request.form.get('grateful1'), request.form.get('grateful2'), request.form.get('grateful3')]
            day_rating = request.form.get('day_rating')

            

            #Create a new journal entry
            journal_entry = Journal(
                date=date,
                user_id=current_user.id,
                dear_journal_content=dear_journal_content,
                grateful_content=','.join(grateful_contents),
                day_rating=day_rating
            )
            
            db.session.add(journal_entry)
            db.session.commit()
            
            list = ["suicide", "murder", "kill", "hurt", "die", "Suicide", "Murder", "Kill", "Hurt", "Die"]
            if any(word in dear_journal_content for word in list):
                db.session.commit()
                flash('Your journal may contain thoughts that may harm yourself or others.', category='error')
                flash('Help is out there. Call 988 or chat online. https://988lifeline.org/chat/', category='error')
            elif any(word in grateful_contents for word in list):
                db.session.commit()
                flash('Your journal may contain thoughts that may harm yourself or others.', category='error')
                flash('Help is out there. Call 988 or chat online. https://988lifeline.org/chat/', category='error')
            return redirect(url_for('views.journal'))
    elif request.method == 'GET':
        previous_entries = Journal.query.filter(Journal.user_id == current_user.id).all()

        previous_entry_id = request.args.get('previous_entry')

        if previous_entry_id:
            selected_entry = Journal.query.get(previous_entry_id)
    date = (datetime.now().date())
    
    return render_template('journal.html', user=current_user, journalTitle=journalTitle, journalSelect=journalSelect, 
                           journalChoose=journalChoose, journalButton=journalButton, journalDate=journalDate, dearJournal=dearJournal, 
                           journalContent=journalContent, gratefulContent=gratefulContent, dayTitle=dayTitle, rating_excellent=rating_excellent, 
                           rating_good=rating_good, rating_bad=rating_bad, rating_horrible=rating_horrible, saveJournal=saveJournal, 
                           journalFooter=journalFooter, previous_entries=previous_entries, selected_entry=selected_entry, date=date)
'''
@views.route('/scanJournal', methods=['POST'])
@login_required
def scan_Journal():
    journal_entry = Journal.query.filter(Journal.date == today, Journal.user_id == current_user.id).first()
    list = ["suicide", "murder", "kill", "hurt"]
    if is_entry_exists_for_today():
        if any(word in journal_entry for word in list):
            db.session.commit()
            return flash('Your journal contained concerning words. What is hurting you?', category='error')
    return jsonify({})
'''
def is_entry_exists_for_today():
    today = date.today()

    entry_for_today = Journal.query.filter(Journal.date == today, Journal.user_id == current_user.id).first()

    return entry_for_today is not None


@views.route('/delete-task', methods=['POST'])
def delete_task():  
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Create a archived with the same data and due date as the original task
        archivedtask = ArchivedTask(data=task.data, user_id=current_user.id, due_date=task.due_date, due_time=task.due_time, date=task.date, was_completed=0)

        # Add and commit changes to the database
        db.session.add(archivedtask)
        db.session.delete(task)
        db.session.commit()

    return jsonify({})

@views.route('/delete-finished-task', methods=['POST'])
def delete_finished_task():  
    task_data = json.loads(request.data)
    finished_task_id = task_data['finishedTaskId']

    finished_task = FinishedTask.query.get(finished_task_id)

    if finished_task and finished_task.user_id == current_user.id:
        # Create a Task with the same data and due date as the FinishedTask
        archivedtask = ArchivedTask(data=finished_task.data, user_id=current_user.id, due_date=finished_task.due_date, due_time=finished_task.due_time, date=finished_task.date, was_completed=1)

        # Add and commit changes to the database
        db.session.add(archivedtask)
        db.session.delete(finished_task)
        db.session.commit()

    return jsonify({})

@views.route('/delete-archived-task', methods=['POST'])
def delete_archivedtask():  
    archivedtask_data = json.loads(request.data)
    archivedTaskId = archivedtask_data['archivedTaskId']
    archivedtask = ArchivedTask.query.get(archivedTaskId)

    if archivedtask and archivedtask.user_id == current_user.id:
        db.session.delete(archivedtask)
        db.session.commit()

    return jsonify({})


@views.route('/mark-task', methods=['POST'])
@login_required
def mark_task():
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Create a FinishedTask with the same data and due date as the original task
        finished_task = FinishedTask(data=task.data, user_id=current_user.id, due_date=task.due_date, due_time=task.due_time, date=task.date)

        # Add and commit changes to the database
        db.session.add(finished_task)
        db.session.delete(task)
        db.session.commit()

    return jsonify({})

@views.route('/star-task', methods=['POST'])
@login_required
def star_task():
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Toggle the starred status
        task.starred = 1 if task.starred != 1 else 0
        db.session.commit()

    return jsonify({})

@views.route('/unmark-task', methods=['POST'])
@login_required
def unmark_task():
    task_data = json.loads(request.data)
    finished_task_id = task_data['finishedTaskId']

    finished_task = FinishedTask.query.get(finished_task_id)

    if finished_task and finished_task.user_id == current_user.id:
        # Create a Task with the same data and due date as the FinishedTask
        task = Task(data=finished_task.data, user_id=current_user.id, due_date=finished_task.due_date, due_time=finished_task.due_time, date=finished_task.date)

        # Add and commit changes to the database
        db.session.add(task)
        db.session.delete(finished_task)
        db.session.commit()

    return jsonify({})


@views.route('/return-task', methods=['POST'])
@login_required
def return_task():
    task_data = json.loads(request.data)
    archived_task_id = task_data['archivedTaskId']

    archived_task = ArchivedTask.query.get(archived_task_id)

    if archived_task and archived_task.user_id == current_user.id and archived_task.was_completed == 0:
        # Create a Task with the same data and due date as the FinishedTask
        task = Task(data=archived_task.data, user_id=current_user.id, due_date=archived_task.due_date, due_time=archived_task.due_time, date=archived_task.date)

        # Add and commit changes to the database
        db.session.add(task)
        db.session.delete(archived_task)
        db.session.commit()

    elif archived_task and archived_task.user_id == current_user.id and archived_task.was_completed == 1:
        finished_task = FinishedTask(data=archived_task.data, user_id=current_user.id, due_date=archived_task.due_date, due_time=archived_task.due_time, date=archived_task.date)

        # Add and commit changes to the database
        db.session.add(finished_task)
        db.session.delete(archived_task)
        db.session.commit()


    return jsonify({})

'''
@views.route('/archive-task', methods=['POST'])
@login_required
def archive_task():
    task_data = json.loads(request.data)
    task_id = task_data['taskId']

    task = Task.query.get(task_id)

    if task and task.user_id == current_user.id:
        # Create an ArchivedTask with the same data, date, and due date as the original task
        archivedtask = ArchivedTask(data=task.data, user_id=current_user.id, due_date=task.due_date, date=task.date)

        # Delete the original task
        db.session.delete(task)
        db.session.commit()

    return jsonify({})
'''
@views.route('/About')
@login_required
def about():
    if current_user.language == "ro":
        about = "Despre Noi"
        aboutDescription1 = "Bine ati venit pe site-ul nostru! Misiunea noastră este să vă facem experiența online cât mai plăcută și informativă posibil cu privire la diferitele opțiuni de sănătate mintală și productivitate disponibile aici. Vă întrebați ce este ProEmPo? Ei bine, ai venit în locul potrivit! ProEmPo este un site web de sănătate mintală și productivitate conceput pentru a promova bunăstarea mintală, pentru a crește gradul de conștientizare cu privire la problemele de sănătate mintală și pentru a oferi resurse și sprijin. De asemenea, oferim resurse productive pentru cei care au nevoie să rămână concentrați pe îndeplinirea sarcinilor."
        aboutDescription2 = "Echipa noastră este pasionată de furnizarea de conținut de înaltă calitate, care să răspundă nevoilor dumneavoastră. Lucrăm în mod constant pentru a îmbunătăți și extinde eforturile noastre pentru a ne asigura că aveți acces la cele mai relevante și interesante informații disponibile."
        aboutDescription3 = "Vă mulțumim că ați vizitat site-ul nostru web și sperăm că îl găsiți util și captivant. Dacă aveți întrebări sau feedback, vă rugăm să nu ezitați "
        contact = "contactaţi-ne"
        aboutDescription4 = "Apreciem contribuția dvs. și așteptăm cu nerăbdare să auzim de la dvs."
    else:
        about = "About Us"
        aboutDescription1 = "Welcome to our website! Our mission is to make your online experience as enjoyable and informative as possible on various mental health and productivity options available here. Are you wondering about what ProEmPo is? Well you came to the right place! ProEmPo is a mental health and productivity website designed to promote mental well-being, raise awareness about mental health issues, and provide resources and support. We also provide productive resources for those in need to stay focused on doing tasks."
        aboutDescription2 = "Our team is passionate about delivering high-quality content that meets your needs. We are constantly working to improve and expand our efforts to ensure that you have access to the most relevant and interesting information available."
        aboutDescription3 = "Thank you for visiting our website, and we hope you find it helpful and engaging. If you have any questions or feedback, please don't hesitate to "
        contact = "contact us"
        aboutDescription4 = "We value your input and look forward to hearing from you."
    return render_template("About.html", user=current_user, about=about, aboutDescription1=aboutDescription1, aboutDescription2=aboutDescription2, aboutDescription3=aboutDescription3, contact=contact, aboutDescription4=aboutDescription4)

@views.route('/settings')
@login_required
def setting():
    
    if current_user.language == "ro":
        selectLanguage = "Selectați limba preferată:"
        title = "Setări"
        save = "Salvează "
        Categories = "Categorii"
        General = "General"
        Accessibility = "Accesibilitate"
        changeuser = "Schimbă Utilizator"
        username = "Utilizator:"
        changepass = "Schimbare Parolă"
        currentpass = "Parolă Curentă"
        newpass = "Parolă Nouă"
        confirmnewpass = "Confirmare Parolă Nouă"
        hidefeatures = "Ascundeți Caracteristici"
        selfhelp = "Ajoutor Personal"
        tasks = "Sarcini"
        dailycheckin = "Verificare Zilnică"
        reports = "Rapoarte"
        language = "Limba"
        oldesttonewest = "Cel mai vechi la cel mai nou"
        newesttooldest = "Cel mai nou la cel mai vechi"
        duedate = "Data scadentă"
        alphabetically = "Alfabetic"
        defaultsort = "Sortare Implicită"
        taskpage = "Pagina de Sarcini"
        starredAtTop = "Afișați Sarcinile Cu Stea În Partea De Sus"
        makeAllButtonsPurple = "Faceți Toate Butoanele Violet"
        player = "Zgomot Alb"
        homepage = "Pagina Principală"
        hidesecondhand = "Ascunde Mâna a Doua"
        hidequote = "Ascunde Citatul Zilei"
    else:
        selectLanguage = "Select your preferred language:"
        title = "Settings"
        save = "Save"
        Categories = "Categories"
        General = "General"
        Accessibility = "Accessibility"
        changeuser = "Change Username"
        username = "Username:"
        changepass = "Change Password"
        currentpass = "Current Password"
        newpass = "New Password"
        confirmnewpass = "Confirm New Password"
        hidefeatures = "Hide Features"
        selfhelp = "Self Help"
        tasks = "Tasks"
        dailycheckin = "Daily Check-In"
        reports = "Reports"
        language = "Language"
        oldesttonewest = "Oldest to Newest"
        newesttooldest = "Newest to Oldest"
        duedate = "Due Date"
        alphabetically = "Alphabetically"
        defaultsort = "Default Sort"
        taskpage = "Task Page"
        starredAtTop = "Show Starred Tasks at Top"
        makeAllButtonsPurple = "Make All Buttons Purple"
        player = "Noise Player"
        homepage = "Home Page"
        hidesecondhand = "Hide Second Hand"
        hidequote = "Hide Quote of the Day"
    return render_template("settings.html",user=current_user, hidequote=hidequote,
                           selectLanguage=selectLanguage, title=title, save=save, Categories=Categories, General=General, Accessibility=Accessibility,
                            changepass=changepass, currentpass=currentpass, newpass=newpass, confirmnewpass=confirmnewpass, 
                            selfhelp=selfhelp, tasks=tasks, dailycheckin=dailycheckin, reports=reports, hidefeatures=hidefeatures,
                            language=language, changeuser=changeuser, username=username, oldesttonewest=oldesttonewest, 
                            newesttooldest=newesttooldest, duedate=duedate, alphabetically=alphabetically, taskpage=taskpage, defaultsort=defaultsort, 
                            starredAtTop=starredAtTop, makeAllButtonsPurple=makeAllButtonsPurple, player=player, homepage=homepage, hidesecondhand=hidesecondhand)


@views.route('/update_starred_at_top', methods=['POST'])
@login_required
def update_starred_at_top():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.starred_at_top = new_value
    db.session.commit()

@views.route('/update_make_all_buttons_purple', methods=['POST'])
@login_required
def update_make_all_buttons_purple():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.make_all_buttons_purple = new_value
    db.session.commit()

@views.route('/update_hide_self_help', methods=['POST'])
@login_required
def update_hide_self_help():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_self_help = new_value
    db.session.commit()

@views.route('/update_hide_quote', methods=['POST'])
@login_required
def update_hide_quote():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_quote = new_value
    db.session.commit()

@views.route('/update_hide_second_hand', methods=['POST'])
@login_required
def update_hide_second_hand():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_second_hand = new_value
    db.session.commit()

@views.route('/update_hide_player', methods=['POST'])
@login_required
def update_hide_player():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_player = new_value
    db.session.commit()

@views.route('/update_hide_tasks', methods=['POST'])
@login_required
def update_hide_tasks():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_tasks = new_value
    db.session.commit()


@views.route('/update_hide_journal', methods=['POST'])
@login_required
def update_hide_journal():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_journal = new_value
    db.session.commit()


@views.route('/update_hide_reports', methods=['POST'])
@login_required
def update_hide_reports():
    user = current_user
    data = request.get_json()
    new_value = data.get('value')
    user.hide_reports = new_value
    db.session.commit()


@views.route('/update_language', methods=['POST'])
@login_required
def update_language():
    user = current_user
    data = request.get_json()
    new_language = data.get('language')
    user.language = new_language
    db.session.commit()

@views.route('/update_defaultsort', methods=['POST'])
@login_required
def update_defaultsort():
    user = current_user
    data = request.get_json()
    new_defaultsort = data.get('defaultsort')
    user.defaultsort = new_defaultsort
    db.session.commit()


@views.route('/General')
@login_required
def general():


    return render_template("General.html", user=current_user)

@views.route('/Accessibility')
@login_required
def accessibility():
    return render_template("Accessibility.html", user=current_user)


@views.route('/Support', methods=['GET'])
def support():
    if current_user.language == "ro":
        supportTitle = "Asistență"

    else:
        supportTitle = "Support"
    support = Support.query.all()
    return render_template("Support.html", user=current_user, supportTitle=supportTitle, support=support)

@views.route('/submit_support', methods=['GET','POST'])
def submit_support_form():

    support_entries = []

    if request.method == 'POST':
        try:
            # Get form data
            new_title = request.form['issue_title']
            new_email = request.form['email']
            new_description = request.form['description']
            if current_user.id != None:
                new_form= Support(user_id=current_user.username,issue_title=new_title, email=new_email,description=new_description)
            else:
                new_form= Support(user_id="No User",issue_title=new_title, email=new_email,description=new_description)
            
            
            db.session.add(new_form)
            db.session.commit()
            
            return render_template('/thank_you.html', user=current_user)
        except Exception as e:
            print("An error occurred while saving the support submission:", e)
            # Handle the error, log it, or take appropriate action
            flash('Failed to submit the support request', category='error')

    return render_template("Support.html", support_entries=support_entries, user=current_user)




@views.route('/ViewFlashcards', methods=["GET", "POST"])
@login_required
def show_flashcard():
    #gets all the cards from the selected user
    lesson_alias = aliased(Lesson)
    user_flashcards = (Card.query.join(lesson_alias).filter(lesson_alias.user_id == current_user.id))

    selected_lesson_id=request.args.get("lesson")
#gets the leasson associated with the card
    if request.method == 'POST':
        selected_lesson_id = request.form.get('lesson')
        if selected_lesson_id and selected_lesson_id != "all":
             user_flashcards=user_flashcards.filter(Card.lesson_id == selected_lesson_id)
#lists out all the cards
    user_flashcards=user_flashcards.all()
#filters all the available lessons by the user
    all_lessons=Lesson.query.filter_by(user_id=current_user.id)
    return render_template("viewFlashcards.html", user=current_user, cards=user_flashcards, all_lessons=all_lessons, select_lesson=selected_lesson_id)


@views.route('/CreateFlashcards', methods=["GET", "POST"])
@login_required
def new_flashcard():
     # gets all the lessons from the user
     
    if request.method == "GET":
        all_lessons=current_user.lessons
        return render_template("createFlashcards.html", all_lessons=all_lessons, user=current_user)
    else:
        #Get the data from the form
        lesson_id=request.form["lesson"]
        question=request.form["question"]
        answer=request.form["answer"]
        new_lesson_name=request.form["new_lesson_name"]

        if lesson_id:
            # Gets the selected lesson from the user
            selected_lesson=Lesson.query.get(lesson_id)
            if not selected_lesson or selected_lesson.user_id != current_user.id:
                print("The selected lesson doesnt exist.")
                return redirect("/CreateFlashcards")
        elif new_lesson_name:
            #Create a new lesson if needed
            new_lesson=Lesson(name=new_lesson_name, user_id=current_user.id)
            db.session.add(new_lesson)
            db.session.commit()
            selected_lesson=new_lesson
        else:
            print("no lesson provided")
            return redirect("/CreateFlashcards")
    
        card=Card(question=question, lesson_id=selected_lesson.id,  answer=answer)
        db.session.add(card)
        db.session.commit()

        return redirect("/CreateFlashcards")

@views.route('/DeleteFlashcard/<int:flashcard_id>', methods=["POST"])
@login_required
def delete_flashcard(flashcard_id):

    flashcard=Card.query.get(flashcard_id)

    db.session.delete(flashcard)
    db.session.commit()

    return redirect("/ViewFlashcards")


@views.route('/ViewFlashcards/<int:flashcard_id>')
@login_required
def get_flashcard(flashcard_id):

    flashcard_id=request.view_args.get('flashcard_id')

    if flashcard_id is None:
        return "Invalid request"

    flashcard=Card.query.get(flashcard_id)

    if not flashcard:
        print('Flashcard not found')
        return redirect('/ViewFlashcards')
    
    return render_template("showFlashcard.html", card=flashcard, user=current_user)



@views.route('/EditFlashcard/<int:flashcard_id>', methods=["GET", "POST"])
@login_required
def edit_flashcard(flashcard_id):

    flashcard = Card.query.get(flashcard_id)

    if flashcard is None:
        flash("Flashcard not found", "error")
        return redirect('/ViewFlashcards')

    if request.method == "POST":
        #get the new values and store them
        lesson_id = request.form.get("lesson")
        question = request.form.get("question")
        answer = request.form.get("answer")

        #new flashcard values assigned 
        flashcard.lesson_id = lesson_id
        flashcard.question = question
        flashcard.answer = answer

        db.session.commit()
        return redirect('/ViewFlashcards/' + str(flashcard_id))
    
    lessons = Lesson.query.filter_by(user_id=current_user.id).all()
    return render_template("editFlashcards.html", card=flashcard, lessons=lessons, user=current_user)

@views.route('/clear-all-completed-tasks', methods=['POST'])
@login_required
def clear_all_completed_tasks():
    completed_tasks = FinishedTask.query.filter_by(user_id=current_user.id).all()

    for task in completed_tasks:
        archived_task = ArchivedTask(
            data=task.data,
            user_id=current_user.id,
            due_date=task.due_date,
            due_time=task.due_time,
            date=task.date,
            was_completed=1
        )

        db.session.add(archived_task)
        db.session.delete(task)

    db.session.commit()

    return jsonify({})



@views.route('/player')
def player():
    playIcon='<i class="fas fa-play"></i>'
    pauseIcon='<i class="fas fa-pause"></i>'

    if current_user.language == "ro":
        whitenoise = "Zgomot Alb"
        birdnoise = "Zgomot de Păsări"
        naturenoise = "Zgomotul Naturii"
        rainnoise = "Zgomot de Ploaie"
        oceannoise = "Zgomot Ocean"
        streamnoise = "Zgomot de Râu"
        underwaternoise = "Zgomot Subacvatic"
        timeplayingnoises = "Timpul de Redare:"
    else:
        whitenoise = "White Noise"
        birdnoise = "Bird Noise"
        naturenoise = "Nature Noise"
        rainnoise = "Rain Noise"
        oceannoise = "Ocean Noise"
        streamnoise = "Stream Noise"
        underwaternoise = "Underwater Noise"
        timeplayingnoises = "Time Playing Noises:"

    return render_template('player.html', user=current_user, playIcon=playIcon, pauseIcon=pauseIcon, whitenoise=whitenoise, birdnoise=birdnoise, naturenoise=naturenoise, rainnoise=rainnoise, oceannoise=oceannoise, streamnoise=streamnoise, underwaternoise=underwaternoise, timeplayingnoises=timeplayingnoises)




@views.route('/goals')
@login_required
def goals():
    user_id = current_user.id
    previous_goals = Goal.query.filter_by(user_id=user_id).all()
    if previous_goals is None:
        previous_goals = [] 

    if current_user.language == "ro":
        mygoals="Obiectivele Mele"
        specific = "Specific"
        measurable = "Măsurabil"
        achievable="Realizabil"
        relevant="Relevant"
        timely="Oportun"
        specificQ="Ce obiectiv voi realiza?"
        measurableQ="Cum o să ştiu că am realizat obiectivul?"
        achievableQ="Obiectivul este realist?"
        relevantQ="De ce este obiectul acesta important?"
        timelyQ="Când voi realiza acest obiectiv?"
        saveGoal="Salvează obiectivul"
        goalCompleted="Obiectiv Terminat"
        seeAllGoals="Vizualizează toate obiectivele"
        explanation1="Când vine vorba de stabilirea obiectivelor, Proempo adoptă abordarea 'smart' a obiectivelor. Abordarea obiectivelor SMART este un cadru profesional de stabilire a obiectivelor cu cinci componente esențiale:"
        explanation2="Specific: Obiectivele trebuie să fie clare și bine definite"
        explanation3="Măsurabile: obiectivele ar trebui să fie cuantificabile"
        explanation4="Realizabil: Obiectivele ar trebui să fie realiste"
        explanation5="Relevant: Obiectivele ar trebui să se alinieze cu obiectivele și valorile dumneavoastră."
        explanation6="Oportune: obiectivele ar trebui să aibă un interval de timp definit"
        explanation7="Acest cadru îmbunătățește precizia și eficacitatea stabilirii obiectivelor."
        answerhere = "Răspunde aici"
        goalsAll = "Toate Golurile"
    else:
        mygoals="My Goals"
        specific = "Specific"
        measurable = "Measurable"
        achievable="Achievable"
        relevant="Relevant"
        timely="Timely"
        specificQ="What goal will I accomplish?"
        measurableQ="How do I know when I reach this goal?"
        achievableQ="Is this goal realistic with commitment?"
        relevantQ="Why is this goal significant to me?"
        timelyQ="When will I achieve this goal?"
        saveGoal="Save My Goal"
        goalCompleted="Goal Completed"
        seeAllGoals="See all goals"
        explanation1="When it comes to goal-setting, Proempo adopts the 'smart' goal approach. The SMART goal approach is a professional goal-setting framework with five essential components:"
        explanation2="Specific: Goals must be clear and well-defined."
        explanation3="Measurable: Goals should be quantifiable and trackable."
        explanation4="Achievable: Goals should be realistic and attainable."
        explanation5="Relevant: Goals should align with your objectives and values."
        explanation6=" Timely: Goals should have a defined time frame."
        explanation7="This framework enhances goal-setting precision and effectiveness."
        answerhere = "Answer here"
        goalsAll = "All Goals"
    return render_template('goals.html', user=current_user, previous_goals=previous_goals, 
                           mygoals=mygoals, specific=specific, measurable=measurable, achievable=achievable, relevant=relevant, 
                           timely=timely, specificQ=specificQ, measurableQ=measurableQ, achievableQ=achievableQ, relevantQ=relevantQ,
                           timelyQ=timelyQ, saveGoal=saveGoal, goalCompleted=goalCompleted, seeAllGoals=seeAllGoals, 
                           explanation6=explanation6, explanation1=explanation1, explanation2=explanation2, 
                           explanation3=explanation3, explanation4=explanation4, explanation5 = explanation5, 
                           explanation7 = explanation7, answerhere=answerhere, goalsAll=goalsAll)



@views.route('/save_goal', methods=['POST'])
def save_goal():
    try:
        data = request.json
        user_id = current_user.id
        specific = data.get('specific')
        measurable = data.get('measurable')
        achievable = data.get('achievable')
        relevant = data.get('relevant')
        timely = data.get('timely')
        status = data.get('status')

        goal_entry = Goal(
            user_id=user_id,
            specific=specific,
            measurable=measurable,
            achievable=achievable,
            relevant=relevant,
            timely=timely,
            status=status
        )

        db.session.add(goal_entry)
        db.session.commit()

        return jsonify({'message': 'Goal entry saved successfully'})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to save goal entry'}), 500


@views.route('/complete_goal/<int:goal_id>', methods=['PUT'])
def complete_goal(goal_id):
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()

        if goal:
            goal.status = "C"
            db.session.commit()
            return jsonify({'message': 'Goal marked as completed successfully'})
        else:
            return jsonify({'message': 'Goal not found or does not belong to the current user'}), 404
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to mark goal as completed'}), 500
    


@views.route('/fetch_goals', methods=['GET'])
@login_required
def fetch_goals():
    user_id = current_user.id
    goals = Goal.query.filter_by(user_id=user_id).all()

    # Serialize the goals to JSON
    serialized_goals = []
    for goal in goals:
        serialized_goal = {
            'id': goal.id,
            'specific': goal.specific,
            'measurable': goal.measurable,
            'achievable': goal.achievable,
            'relevant': goal.relevant,
            'timely': goal.timely,
            'status': goal.status
        }
        serialized_goals.append(serialized_goal)

    return jsonify({'goals': serialized_goals})


def get_iso_year_week(date):
    year, week, _ = date.isocalendar()
    return year, week

@views.route('/accomplishments', methods=['GET', 'POST'])
@login_required
def pride():
    if current_user.language == "ro":
        accomplishmentsTitle = "Realizări"
        accomplishmentsDescription1 = "Fă-ți timp pentru a reflecta asupra realizărilor și calităților care te fac să fii mândru de tine."
        accomplishmentsDescription2 = "Îmbrățișarea călătoriei tale este un proces unic și continuu, unul care se referă la tine."
        accomplishmentsDescription3 = "Enumerați mai jos până la 5 calități de care sunteți mândru și reveniți pe această pagină când vă simțiți dezamăgiți."
        accomplishmentsDescription4 = "Ține minte: ești capabil de lucruri minunate."
        accomplishmentsQuestion = "De ce esti mandru?"
        saveAccomplishments = "Salvați"
        proud = "Sunt mândru de..."
        placeholder = "Enumerați aici de ce sunteți mândru..."
        accomplishmentsWarning = "Sigur vrei să ștergi această postare?"
    else:
        accomplishmentsTitle = "Accomplishments"
        accomplishmentsDescription1 = "Take some time to reflect on the accomplishments and qualities that make you proud of yourself."
        accomplishmentsDescription2 = "Embracing your journey is a unique and ongoing process, one that's all about you."
        accomplishmentsDescription3 = "List up to 5 qualities that you are proud of below and come back to this page when you are feeling down."
        accomplishmentsDescription4 = "Remember: you are capable of wonderful things."
        accomplishmentsQuestion = "What are you proud of?"
        saveAccomplishments = "Save"
        proud = "I am proud of..."
        placeholder = "List what you are proud of here..."
        accomplishmentsWarning = "Are you sure you want to delete this post?"
    current_year, current_week_number = get_iso_year_week(today)

    recent_accomplishments = Pride.query.filter(
        Pride.user_id == current_user.id,
        Pride.year == current_year,
        Pride.week_number == current_week_number,
        Pride.status == False
    ).all()


    for accomplishment in recent_accomplishments:
        #Update the status once it lands outside the current week
        if current_week_number - accomplishment.week_number > 0:
            accomplishment.status = True 
    
    if request.method == 'POST':
        #max entries for the week check
        maximum_entries = 5
        entries_for_week = len(recent_accomplishments)

        if entries_for_week >= maximum_entries:
            flash("You have entered the maximum number of entries. Only 5 per week")
        else:
            new_moment = request.form.get('moment')
            pride_entry = Pride(
            user_id=current_user.id,
            moment=new_moment,
            year=current_year,
            week_number=current_week_number,
            status=False,
        )

            db.session.add(pride_entry)
            db.session.commit()
            
    recent_accomplishments = Pride.query.filter(
        Pride.user_id == current_user.id,
        Pride.year == current_year,
        Pride.week_number == current_week_number,
        Pride.status == False
    ).all()
    
    return render_template('pride.html', recent_accomplishments=recent_accomplishments, 
                           user=current_user, accomplishmentsTitle=accomplishmentsTitle, 
                           accomplishmentsDescription1=accomplishmentsDescription1, accomplishmentsDescription2=accomplishmentsDescription2,
                           accomplishmentsDescription3=accomplishmentsDescription3, accomplishmentsDescription4=accomplishmentsDescription4,
                           accomplishmentsQuestion=accomplishmentsQuestion, saveAccomplishments=saveAccomplishments, proud=proud, 
                           placeholder=placeholder, accomplishmentsWarning=accomplishmentsWarning)
    

@views.route('/DeletePride/<int:pride_id>', methods=["POST"])
@login_required
def delete_pride(pride_id):

    moment=Pride.query.get(pride_id)
    db.session.delete(moment)
    db.session.commit()
    
    return redirect(url_for('views.pride'))
    
@views.route('/past-accomplishments', methods=['GET', 'POST'])
@login_required
def past_week_accomplishments():

    error_message = ""

    past_accomplishments = Pride.query.filter(
        Pride.user_id == current_user.id,
        Pride.status == True
    ).order_by(Pride.date.desc()).limit(5).all()

    if not past_accomplishments:
        error_message = "You havent listed any accomplishments in the past week"

    return render_template('pastAccomplishments.html', past_accomplishments=past_accomplishments,error_message=error_message, user=current_user)