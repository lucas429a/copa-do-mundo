from rest_framework.views import APIView, status, Request, Response
from teams.models import Team
from django.forms import model_to_dict
from teams.utils import data_processing
from teams.exceptions import NegativeTitlesError, ImpossibleTitlesError, InvalidYearCupError


class TeamView(APIView):

    def post(self, request: Request) -> Response:
        data = request.data
        try:
            data_processing(data)
            team = Team.objects.create(**data)
            team.save()
            converted_team = model_to_dict(team)
            return Response({converted_team, status.HTTP_201_CREATED})
        except (
            NegativeTitlesError,
            InvalidYearCupError,
            ImpossibleTitlesError
        ) as err:
            return Response({"error": err.args[0]}, status.HTTP_400_BAD_REQUEST)    

    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        converted_teams = []
        for team in teams:
            converted_team = model_to_dict(team)
            converted_teams.append(converted_team)
        return Response(converted_teams, status.HTTP_200_OK)


class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"error": "time não encontrada."},
                status.HTTP_404_NOT_FOUND,
            )
        converted_team = model_to_dict(team)
        return Response(converted_team)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"error": "time não encontrada."},
                status.HTTP_404_NOT_FOUND,
            )
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
            for key, value in request.data.items():
                setattr(team, key, value)
                team.save()
                converted_team = model_to_dict(team)
            return Response(converted_team)
        except (
            NegativeTitlesError,
            InvalidYearCupError,
            ImpossibleTitlesError
        ) as err:
            return Response({"error": err.args[0]}, status.HTTP_400_BAD_REQUEST)