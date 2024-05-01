import os

from typing import List

from inquirer import List as PList
from inquirer import Checkbox, prompt, Text


QUESTION_NAME = "TEMP"
MULTIPLE_CHOICE_QUESTION_ADDITION = " Press [space] on each option you want to select. Press [enter] when you want to submit your selection."


def askMultipleChoiceQuestion(message: str, options: List[str]) -> List[str]:
    """
    ::
        Ask for the user to select several choices from a list of options.
    
    Parameters:
        (str) message:          The prompt to print to the user upon asking for the user input.
        (List[str]) options:    The options the user needs to choose from.
    
    Returns:
        (List[str]):            A list of the options the user chose.
    """
    return prompt([Checkbox(QUESTION_NAME, message=message + MULTIPLE_CHOICE_QUESTION_ADDITION, choices=options)])[QUESTION_NAME]


def askSingleChoiceQuestion(message: str, options: List[str]) -> str:
    """
    ::
        Ask for the user to select a choice from a list of options.
    
    Parameters:
        (str) message:          The prompt to print to the user upon asking for the user input.
        (List[str]) options:    The options the user needs to choose from.
    
    Returns:
        (str):                  The option the user chose.
    """
    return prompt([PList(QUESTION_NAME, message=message, choices=options)])[QUESTION_NAME]


def askUserInput(message: str) -> str:
    """
    ::
        Ask user to enter input.
    
    Parameters:
        (str) message:          The prompt to print to the user upon asking for the user input.
    
    Returns:
        (str):                  The user input.
    """
    return prompt([Text(QUESTION_NAME, message=message)])[QUESTION_NAME]


def clearCli() -> None:
    os.system("cls")