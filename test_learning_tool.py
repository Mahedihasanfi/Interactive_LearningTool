import pytest
from unittest.mock import patch
import random

# Import the LearningTool class
from learning_tool import LearningTool, Question


@pytest.fixture
def learning_tool():
    return LearningTool()


def test_disable_enable_question(learning_tool):
    # Add a question
    id = random.randint(100, 50000)
    question = Question(
        id,
        "Test question",
        "quiz",
        options=["Option 1", "Option 2"],
        correct_answer="1",
        active=True,
    )
    learning_tool.questions.append(question)

    # Test disabling the question
    with patch("builtins.input", side_effect=[id, "disable"]):
        learning_tool.disable_enable_question()
    assert not question.active

    # Test enabling the question
    with patch("builtins.input", side_effect=[id, "enable"]):
        learning_tool.disable_enable_question()
    assert question.active


def test_view_statistics(learning_tool):
    # Add some questions
    id = random.randint(100, 50000)
    question = Question(
        id,
        "Test question",
        "quiz",
        options=["Option 1", "Option 2"],
        correct_answer="1",
        active=True,
        times_shown=5,
        times_correct=3,
    )
    learning_tool.questions.append(question)

    # Test view statistics
    with patch("builtins.print") as mock_print:
        learning_tool.view_statistics()

    mock_print.assert_any_call("Question Statistics:")
    mock_print.assert_any_call(f"Question ID: {id}")
    mock_print.assert_any_call("Question Text: Test question")
    mock_print.assert_any_call("Active: True")
    mock_print.assert_any_call("Times Shown (Practice): 5")
    mock_print.assert_any_call("Percentage Correct: 60.00%")


def test_profile_statistics_existing_profile(learning_tool):
    # Set up an existing profile with some statistics
    learning_tool.profile = "profile1"
    learning_tool.profiles = {
        "profile1": {"Score": 5, "TotalQuestions": 10, "TimesCorrect": 3}
    }

    # Test profile statistics
    with patch("builtins.print") as mock_print:
        learning_tool.profile_statistics()

    # Verify the expected output was printed
    mock_print.assert_any_call("\nYour Personal Profile Statistics:")
    mock_print.assert_any_call("Profile: profile1")
    mock_print.assert_any_call("Score: 5")
    mock_print.assert_any_call("Total Questions: 10")
    mock_print.assert_any_call("Times Correct: 3")


if __name__ == "__main__":
    test_disable_enable_question()
    test_view_statistics()
    test_profile_statistics_existing_profile()
