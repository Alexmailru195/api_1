from .models import QuestionCategory
from .serializers import QuestionCategorySerializer, QuestionSerializer, AnswerSerializer
from .paginators import QuizResultsSetPagination
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Answer
from rest_framework.decorators import api_view


@api_view(['POST'])
def check_answer(request):
    try:
        question_id = request.data.get('question_id')
        answer_id = request.data.get('answer_id')

        question = Question.objects.get(id=question_id)
        answer = Answer.objects.get(id=answer_id, question=question)

        return Response({
            "question_text": question.text,
            "is_correct": answer.is_correct
        }, status=status.HTTP_200_OK)

    except Question.DoesNotExist:
        return Response({"error": "Вопрос не найден"}, status=status.HTTP_404_NOT_FOUND)
    except Answer.DoesNotExist:
        return Response({"error": "Ответ не связан с вопросом"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({"error": "Неверные данные"}, status=status.HTTP_400_BAD_REQUEST)


class QuestionCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer


class QuestionCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionCategory.objects.all()
    serializer_class = QuestionCategorySerializer


class QuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = QuizResultsSetPagination


class QuestionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
