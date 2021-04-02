# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import os
import ask_sdk_core.utils as ask_utils
import random
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


acts = ['rock','paper','scissor']

class HasPlayedLaunchRequestHandler(AbstractRequestHandler):
    """Handler for Has Played Launch Request."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr=handler_input.attributes_manager.persistent_attributes
        attributes_are_present=("alexa_score" in attr and "user_score" in attr and "times_played" in attr)
        return (attributes_are_present and ask_utils.is_request_type("LaunchRequest")(handler_input))
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr=handler_input.attributes_manager.persistent_attributes
        alexa_score=int(attr['alexa_score'])
        user_score=int(attr['user_score'])
        times_played=int(attr['times_played'])
        
        if times_played>=1:
            speak_output=("Heya!, Welcome back. You have played {} times. Your score: {}, My score: {}. Let's play again. "
                          "Choose Rock or Paper or Scissors. ".format(times_played,user_score,alexa_score))
        else:
            speak_output="Let's start playing. Choose one. Rock or Paper or Scissor. "
            
        reprompt_text="What did you choose? Rock or Paper or Scissors?. "
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        score_attr={'alexa_score':0,'user_score':0,'times_played':0}
        handler_input.attributes_manager.persistent_attributes=score_attr
        handler_input.attributes_manager.save_persistent_attributes()
        speak_output = ("Heya, Here's Rock Paper Scissor. "
                        "Say Yes to start playing. "
                        "You can say help for Game Rules. ")
        reprompt = "What's your choice? "
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response)


class NewGameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NewGameIntent")(handler_input)

    def handle(self, handler_input):
        score_attr={'alexa_score':0,'user_score':0,'times_played':0}
        handler_input.attributes_manager.persistent_attributes=score_attr
        handler_input.attributes_manager.save_persistent_attributes()
        speak_output = ("Heya, Here's a new game. "
                        "Say Yes to start playing. "
                        "You can say help for Game Rules. ")
        reprompt = "What's your choice? "
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response)



class GetActIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetActIntent")(handler_input)
        
    def handle(self, handler_input):
        #n = random.randint(0,len(acts)-1)
        alexa_action = random.choice(acts)
        slots = handler_input.request_envelope.request.intent.slots
        user_action = slots["action"].value        
        
        attr=handler_input.attributes_manager.persistent_attributes
        alexa_score=int(attr['alexa_score'])
        user_score=int(attr['user_score'])
        times_played=int(attr['times_played'])
        
        if user_action == 'scissor':  
            if alexa_action == 'rock':
                alexa_score += 1
                speak_output= "I win! Woot! Woot! Paper beats rock. You know what to do. What's your choice? "        
            elif alexa_action == 'paper':
                user_score += 1
                speak_output= "You won. Awesome!. Let's play again. What do you choose? "
            elif alexa_action == 'scissor':
                speak_output= "It's a tie. Let's play again. Choose One. Rock or Paper or Scissor. "

            
        elif user_action == 'paper':
            if alexa_action == 'scissor':
                alexa_score += 1
                speak_output= "I won. Scissor cuts paper. Give it one more try. What do you choose? "  
            elif alexa_action == 'rock':
                user_score += 1
                speak_output= "Paper covers rock. You won. Well done!. Let's play one more round. "  
            elif alexa_action == 'paper':
                speak_output= "Ahem. How about we play something different next time! Again! Rock or Paper or Scissor. "

            
        elif user_action == 'rock':
            if alexa_action == 'paper':
                alexa_score += 1
                speak_output= "Rock crushes scissors. I owned that round. You know the drill. Rock or Paper or Scissor. "
            elif alexa_action == 'scissor':
                user_score += 1
                speak_output= "Woah!. You are playing well. You won. What do you choose? "
            elif alexa_action == 'rock':
                speak_output= "How did you know what I was going to play? One more time, Rock paper or scissors? " 
        
        score_attr={'alexa_score':alexa_score,'user_score':user_score,'times_played':times_played}
        handler_input.attributes_manager.persistent_attributes=score_attr
        handler_input.attributes_manager.save_persistent_attributes()
        
        reprompt = "What do you choose?. "

        return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)



class GetScoreIntentHandler(AbstractRequestHandler):
    """Handler for Tell Score Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return  ask_utils.is_intent_name("GetScoreIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr=handler_input.attributes_manager.persistent_attributes
        user_score=int(attr['user_score'])
        alexa_score=int(attr['alexa_score'])
        
        speak_output = "Your Score: {}, My Score: {}. Let's resume playing. What is your choice? ".format(user_score,alexa_score)
        
        reprompt_text="Rock or Paper or Scissor. What do you choose? "
        
        return (handler_input.response_builder.speak(speak_output).ask(reprompt_text).response)



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ("Rock crushes Scissor, Paper Wins against Rock, Scissor cuts Paper. "
                        "You can say 'Score' to get the score updates. "
                        "You can say 'New Game' to start a new game. "
                        "You can say 'Stop' to end the game. "
                        "Let's start playing. Try saying Rock or Paper or Scissor. ")
        reprompt = "Try saying rock, paper or scissor. "

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class YesHandler(AbstractRequestHandler):
    # type: (HandlerInput) -> Response
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)
    
    def handle(self , handler_input):
        
        speech_text = ("Awesome. Let's start playing. "
                       "You can ask for Score anytime. "
                       "You can start with a new game anytime. "
                       "You can Stop the game whenever you want. "
                       "What do you choose? Rock or Paper or Scissor. ")
        reprompt = "Try saying Rock or Paper or Scissor. "
        return (handler_input.
                response_builder.
                speak(speech_text).
                ask(reprompt).
                response)



class NoHandler(AbstractRequestHandler):
    # type: (HandlerInput) -> Response
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)
    
    def handle (self , handler_input):
        speech_text = "Try saying Rock or Paper or Scissor! "
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response



class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr=handler_input.attributes_manager.persistent_attributes
        user_score=int(attr['user_score'])
        alexa_score=int(attr['alexa_score'])
        times_played=int(attr['times_played'])
        
        if (alexa_score!=0 or user_score!=0):
            times_played+=1
        
        if user_score>alexa_score:
            speak_output = "Congrats! You are the Winner. Your Score: {}, My Score: {}. Goodbye. ".format(user_score,alexa_score)
        elif user_score<alexa_score:
            speak_output = "Yippie!. I am the Winner. Better luck next time. Your Score: {}, My Score: {}. Goodbye. ".format(user_score,alexa_score)
        elif alexa_score==user_score and alexa_score!=0 and user_score!=0:
            speak_output = "Both of us think so similar. It's a Tie. Your Score: {}, My Score: {}. Goodbye. ".format(user_score,alexa_score)
        elif alexa_score==0 and user_score==0:
            speak_output = "You haven't played yet. Hope you come back soon. Goodbye. ".format(user_score,alexa_score)

            
        score_attr={'alexa_score':alexa_score,'user_score':user_score,'times_played':times_played}
        handler_input.attributes_manager.persistent_attributes=score_attr
        handler_input.attributes_manager.save_persistent_attributes()

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.
        attr=handler_input.attributes_manager.persistent_attributes
        user_score=int(attr['user_score'])
        alexa_score=int(attr['alexa_score'])
        times_played=int(attr['times_played'])
        
        if (alexa_score!=0 or user_score!=0):     
            times_played+=1
        speak_output = "Your score: {}, My score: {}. Goodbye. ".format(user_score,alexa_score)
        
        score_attr={'alexa_score':alexa_score,'user_score':user_score,'times_played':times_played}
        handler_input.attributes_manager.persistent_attributes=score_attr
        handler_input.attributes_manager.save_persistent_attributes()
        
        return handler_input.response_builder.response



class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I did'nt understand what you said."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(HasPlayedLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NewGameIntentHandler())
sb.add_request_handler(GetActIntentHandler())
sb.add_request_handler(GetScoreIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(YesHandler())
sb.add_request_handler(NoHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()