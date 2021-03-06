from chatterbot.logic import LowConfidenceAdapter
from chatterbot.conversation import Statement
from tests.base_case import ChatBotTestCase


class LowConfidenceAdapterTestCase(ChatBotTestCase):
    """
    Test cases for the LowConfidenceAdapter.
    """

    def setUp(self):
        super().setUp()
        self.adapter = LowConfidenceAdapter(self.chatbot)

        self.chatbot.storage.create(
            text='Who do you love?',
            in_response_to='I hear you are going on a quest?'
        )
        self.chatbot.storage.create(
            text='What is the meaning of life?',
            in_response_to='Yuck, black licorice jelly beans.'
        )
        self.chatbot.storage.create(
            text='I am Iron Man.',
            in_response_to='What... is your quest?'
        )
        self.chatbot.storage.create(
            text='What... is your quest?',
            in_response_to='I am Iron Man.'
        )
        self.chatbot.storage.create(
            text='Yuck, black licorice jelly beans.',
            in_response_to='What is the meaning of life?'
        )
        self.chatbot.storage.create(
            text='I hear you are going on a quest?',
            in_response_to='Who do you love?'
        )

    def test_high_confidence(self):
        """
        Test the case that a high confidence response is known.
        """
        statement = Statement(text='What is your quest?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match, self.adapter.default_responses[0])

    def test_low_confidence(self):
        """
        Test the case that a high confidence response is not known.
        """
        statement = Statement(text='Is this a tomato?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match, self.adapter.default_responses[0])

    def test_low_confidence_options_list(self):
        """
        Test the case that a high confidence response is not known.
        """
        self.adapter.default_responses = [
            Statement(text='No')
        ]

        statement = Statement(text='Is this a tomato?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match, 'No')
