from .models import Participation


def is_campaign_director(user, campaign):
    if not user.is_authenticated:
        return False

    return campaign.director == user


def is_campaign_participant(user, campaign):
    if not user.is_authenticated:
        return False

    return Participation.objects.filter(
        user=user,
        campaign=campaign,
        status=Participation.Status.ACCEPTED,
    ).exists()


def can_view_campaign(user, campaign):
    if campaign.visibility == campaign.Visibility.PUBLIC:
        return True

    return (
        is_campaign_director(user, campaign)
        or is_campaign_participant(user, campaign)
    )