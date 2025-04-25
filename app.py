from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 👇 Your 5 quiz questions
quiz = [
    {
        "question": "Which country is known for inventing Volleyball?",
        "options": ["Brazil", "Japan", "United States", "Russia"],
        "answer": "United States",
        "fact": "🏐 Did you know? Volleyball was invented way back in 1895 in Massachusetts, USA by a guy named William G. Morgan!👴💪 \n \n He originally created it as a less intense alternative to basketball — especially for older members at his local YMCA gym. \n \n So yeah... volleyball started out as the chill cousin of basketball 😎🏀➡️🏐"
    },
    {
        "question": "Why should you not cook honey at high temperatures for too long?",
        "options": ["It turns into alcohol", "It releases free radicals", "It produces toxic compound", "It ferments instantly"],
        "answer": "It produces toxic compound",
        "fact": "If honey is cooked too long or at too high a temperature, it can create a toxic compound called HMF (Hydroxymethylfurfural) 🧪 \n \n🐝💡 Fun fact: Beekeepers actually use HMF levels to check honey quality! \n  🔍 High HMF = old or overheated honey"
    },
    {
        "question": "Why do carbonated drinks cause tingling sensation on your tongue?",
        "options": ["the bubbles irritate your taste bud", "the sugar interacts with your saliva", "your tongue senses a weak acid", "the pressure from the fizz numbs your tongue"],
        "answer": "your tongue senses a weak acid",
        "fact": "🥤 Fun Fact! Joseph Priestley, the guy who discovered oxygen — also started infusing water with carbon dioxide! 💨💧 \n \n He thought the fizzy bubbles might help with digestive problems, and called it medicated water 🧪💊 \n \n So yeah… modern sodas are basically a 19th-century health tonic in disguise 😄💁‍♂️✨"
    },
    {
        "question": "What was Sanji's original name before Oda changed it during the early draft of the series?",
        "options": ["Naruto", "Reiji", "Sabato", "Vincent"],
        "answer": "Naruto",
        "fact": "👨‍🍳🍥 Eiichiro Oda originally wanted to name Sanji: Naruto! Because of narutomaki 🍥🍥 — which fit his chef aesthetic perfectly! 🍜✨ \n \n To avoid confusion with the series Naruto, Oda changed the name to Sanji — which actually means three in Japanese, and it turns out he is the third son of the Vinsmoke family 👑 \n \n🧠💥 What a perfect foreshadowing move from Oda!"
    },
    {
        "question": "What unique power does the Attack Titan possess compared to the other Nine Titans?",
        "options": ["It can harden instantly", "It can see the memories of future inheritors", "It can control other titans", "It can fly"],
        "answer": "It can see the memories of future inheritors",
        "fact": "💥 The Attack Titan is built different: Unlike the other Titans, its special power is REBELLION. 🖤⚔️ \n \n The Attack Titan can access memories of future inheritors, meaning people like Grisha Yeager saw visions from Eren decades before Eren even got the Titan. 😱🧬 And yeah — it completely changed Grisha choices, shaping the entire story. \n \nSo basically? The Attack Titan does not just fight enemies ➡️ It fights destiny itself. 🌀🔥"
    },
    {
        "question": "Which of the following flowers used to help clean up radioactive soil?",
        "options": ["Lavender", "Rose", "Cherry Blossom", "Sunflower"],
        "answer": "Sunflower",
        "fact": "🌻 Did you know? Sunflowers were actually planted at nuclear disaster sites like Chernobyl and Fukushima! 😮 \n Why? Because they absorb radioactive isotopes from the soil — all thanks to a process called phytoremediation 🌱⚛️ \n \n But that's not all! Sunflowers are also used to clean up: \n 🏙️ Lead-contaminated urban soils \n 🛢️ Oil spills \n ⚠️ Water polluted with heavy metals \n \n So yeah... sunflowers are nature cleanup crew 💛🌍🧼"
    },
    {
        "question": "Which color literally did not exist in ancient language - even as a concept?",
        "options": ["Red", "Green", "Blue", "Yellow"],
        "answer": "Blue",
        "fact": "In ancient texts, the sea was often described as wine-dark — not blue! 🍷🌊 Weird, right? \n \n That’s because ancient languages like Greek, Chinese, Japanese, and Hebrew didn’t even have a distinct word for blue! 🤯\n \n It’s believed that people back then didn’t see blue the way we do — they saw it as just a shade of black or green 👁️💚🖤\n So yeah… the color blue is kinda new to the human brain! 🎨🧠"
    },
    {
        "question": "What is the original meaning of the name Eren from Eren Yeager?",
        "options": ["Storm Bringer in Old German", "Saint in Turkish", "Fated one in Latin", "Revolution in ancient greek"],
        "answer": "Saint in Turkish",
        "fact": "⚔️ Isayama loves flipping expectations — and the irony runs deep. \nEren's name in Turkish means saint or holy person🕊️ \n \n But instead of becoming humanity’s savior… He becomes the Devil of Paradis 😈🌍"
    }
]

# Optional: fun reaction messages
correct_reactions = [
    "Correct! 🎉 You're crushing it!",
    "Boom! Nailed it! 💥",
    "Yes!! You got it! 🧠",
    "Well done! 🎯",
    "You're on fire! 🔥"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "").lower()
    index = data.get("index")

    # First quiz start triggers
    if "sleepy" in msg:
        return first_quiz("Oh nooo.. I bet a quiz could help you feel energized 😴⚡")
    elif "tired" in msg:
        return first_quiz("Ok after the quiz I'll give you a perfeeect massage 😏")
    elif "ok" in msg:
        return jsonify({
            "response": "Bruh.. seriously? Just OK?? 😑",
            "options": ["I mean... SUPER EXCITEDDDDDD"]
        })
    elif "excited" in msg:
        return first_quiz("Ohaaaa chill, here comes the quiz! 🤩")

    # Quiz flow — check answer using index
    if index is not None and index != "reward":
        try:
            index = int(index)
            current_q = quiz[index]
            correct_answer = current_q["answer"].lower()

            if msg == correct_answer.lower():
                next_index = index + 1
                fact_text = current_q.get("fact", "")
                if next_index < len(quiz):
                    next_q = quiz[next_index]
                    return jsonify({
                        "response": random_reaction(),
                        "next": {
                            "response": fact_text,
                            "followup": {
                                "response": f"Q{next_index + 1}: {next_q['question']}",
                                "options": next_q["options"],
                                "index": next_index
                            }
                        }
                    })
                else:
                    return jsonify({
                        "response": "Well done! 🎯 Now you are a quiz master",
                        "next": {
                            "response": "Now you can choose your reward! 🎁",
                            "options": ["Reward 1", "Reward 2", "Reward 3", "Reward 4"],
                            "index": "reward",
                            "claimed": []
                        }
                    })

            else:
                return jsonify({
                    "response": "Oops! That's not quite right. Try again! 😬",
                    "options": current_q["options"],
                    "index": index
                })
        except:
            return jsonify({"response": "Something went wrong while checking your answer."})
    
    if index == "reward":
        claimed = data.get("claimed", [])
        rewards = {
            "Reward 1" : {
                "type" : "link",
                "content" : "I made you a little card to celebrate your special day! 💖 👉 <a href='https://online.fliphtml5.com/bruhz/gnkv/' target='_blank'>Open your card</a>"
            },
            "Reward 2" : {
                "type" : "image",
                "content" : "/static/Lego.png",
                "confetti": True
            },
            "Reward 3" : {
                "type" : "image",
                "content" : "/static/Gift.png",
                "confetti": True
            },
            "Reward 4" : {
                "type" : "link",
                "content" : "Oh looks like your friends also wanted to celebrate together! 💌 👉 <a href='https://www.kudoboard.com/boards/3crijJNT' target='_blank'>What are they saying?</a>"
            }
        }
        
        selected = next((r for r in rewards if msg.strip().lower() == r.lower()), None)
        if not selected:
            return jsonify({"response": "Hmm, I didn’t recognize that reward."})

        if selected not in claimed:
            claimed.append(selected)

        reward = rewards[selected]
        response_data = {
            "response": f"You claimed: {selected} 🎉",
            "next": {
                "index": "reward",
                "claimed": claimed
            }
        }

        if reward["type"] == "link":
            response_data["next"]["response"] = reward["content"]
        elif reward["type"] == "image":
            response_data["next"]["response"] = f"<img src='{reward['content']}' alt='{selected}' style='max-width:100%; border-radius:10px;'>"
            if reward.get("confetti"):
                response_data["next"]["confetti"] = True

        if len(claimed) == len(rewards):
            response_data["next"]["followup"] = {
                "response": "Thank you for playing! 🥳 You deserve all the happiness and love in life. \n Welcome to your new age, you oldie!🎉"
            }
        else:
            remaining = [r for r in rewards if r not in claimed]
            response_data["next"]["options"] = remaining

        return jsonify(response_data)

    # Default fallback
    return jsonify({
        "response": "Say how you're feeling first!",
        "options": ["Sleepy", "I'm OK", "Super Excited", "Tired"]
    })



def first_quiz(reaction_text):
    return jsonify({
        "response": reaction_text,
        "next": {
            "response": f"Q1: {quiz[0]['question']}",
            "options": quiz[0]["options"],
            "index": 0
        }
    })

def random_reaction():
    import random
    return random.choice(correct_reactions)

if __name__ == "__main__":
    app.run(debug=True)
