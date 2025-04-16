from flask import Flask, render_template
import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from threading import Lock, Event

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")

egg_info_flag_key = "tell-a-joke"

def show_evaluation_result(key: str, value: bool):
    print()
    print(f"*** The {key} feature flag evaluates to {value}")


# List of egg facts
egg_facts = [
    "The largest chicken egg ever laid weighed 12 ounces!",
    "Eggs contain all 9 essential amino acids.",
    "The color of an egg's shell is determined by the breed of the chicken.",
    "Eggs can be stored in the refrigerator for up to 5 weeks.",
    "The average hen lays 300-325 eggs per year.",
    "Eggs are one of the few foods that naturally contain Vitamin D.",
    "The world record for most eggs laid by a chicken in one day is 7.",
    "Eggs are considered a complete protein source.",
    "The yolk color depends on the hen's diet.",
    "Eggs are one of the most versatile ingredients in cooking."
]

# List of egg jokes (question and answer)
egg_jokes = [
    {"question": "Why did the egg go to school?", "answer": "To get egg-ucated!"},
    {"question": "What do you call an egg from outer space?", "answer": "An egg-stra terrestrial!"},
    {"question": "Why did the Easter egg hide?", "answer": "Because it was a little chicken!"},
    {"question": "What do you call an egg that's afraid of everything?", "answer": "A chicken!"},
    {"question": "Why did the egg cross the road?", "answer": "To prove he wasn't a chicken!"},
    {"question": "What do you call an egg that's always late?", "answer": "An egg-stra slow egg!"},
    {"question": "Why was the Easter egg so good at stand-up comedy?", "answer": "Because it always cracked people up!"},
    {"question": "How do you send a letter to an Easter egg?", "answer": "By egg-spress delivery!"},
    {"question": "Why did the egg get promoted?", "answer": "Because it was egg-cellent at its job!"},
    {"question": "What do you call an egg that's a great dancer?", "answer": "An egg-straordinary mover!"}
]

@app.route("/")
def home():
    # Set up the evaluation context
    context = Context.builder("example-user-key").kind("user").name("Sandy").build()

    # Check the value of the feature flag
    egg_info_flag_key_value = ldclient.get().variation(egg_info_flag_key, context, False)

    # Render different templates based on the flag value
    # if true, share a joke
    if egg_info_flag_key_value:
        return render_template('jokes.html', jokes=egg_jokes)
    # if false, share a fact
    else:
        return render_template('index.html', facts=egg_facts)

if __name__ == "__main__":
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()
    if not egg_info_flag_key:
        print("*** Please set the LAUNCHDARKLY_FLAG_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))

    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    print("*** SDK successfully initialized")

    # Set up the evaluation context. This context should appear on your
    # LaunchDarkly contexts dashboard soon after you run the demo.
    context = \
        Context.builder('example-user-key').kind('user').name('Sandy').build()

    # Check the value of the feature flag.
    # check if the variable value names are correct

    egg_info_flag_value = ldclient.get().variation(egg_info_flag_key, context, False)

    show_evaluation_result(egg_info_flag_key, egg_info_flag_value)
    
    try:
        app.run(debug=True)
        Event().wait()
    except KeyboardInterrupt:
        pass