from skills import Skills
from intent import IntentCheck
import spacy

if __name__ == '__main__':

    # load intent check model
    intentCheck = IntentCheck()

    # load and initialize spacy for entity recognition, use 
    #   https://explosion.ai/demos/displacy
    nlp = spacy.load("en_core_web_sm") #lg

    # load skills
    skills = Skills()

    # speak a greeting from the greeting skill
    message = skills.skills['greeting'].actAndGetResponse()

    while True:

        # get new command
        command = input("DBG> ")

        # interpret command for intent
        intent = intentCheck.getIntentFromString(command)

        # initialize standard set of parameters
        params = {'intentCheck': intentCheck, 'skills': skills.skills} 

        try: # find and execute skill
            skill = skills.skills[intent]
            params |= skill.parseEntities(nlp(command))
            print(params)

            response = skill.actAndGetResponse(**params)
            print(response)
        except Exception as e:
            print(e)
            # vocal_output.say("Could not find skill, bye.")
            # break
