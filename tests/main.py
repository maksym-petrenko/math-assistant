import os

from chatgpt.convert_to_mathematica import convert
from wolfram.helper import get_step_by_step_solution


class TestClass:

    def test_text_processing(self):
        """Test ChatGPT + Wolfram performance on input strings."""

        files = os.listdir('test_data/texts/questions')
        questions_dir = 'test_data/texts/questions/'
        answers_dir = 'test_data/texts/answers/'

        for file_path in files:
            with open(questions_dir + file_path) as question, open(answers_dir + file_path) as answer:
                converted = convert(question.read())
                solved = get_step_by_step_solution(converted, 'image')[0]['alt']
                assert solved == answer.read()
