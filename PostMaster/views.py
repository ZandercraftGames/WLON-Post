from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ratelimit.decorators import ratelimit

import PostMaster.models
from PostMaster.models import Nation, Tracking, Package
from PostMaster.forms import SearchForm, SubscribeForm
from uuid import UUID

# Constants
api_ratelimit = '4/s'


# ------------------------- #
#   Public Frontend Views   #
# ------------------------- #

def index(request):
    """
    Returns a rendered index page for the site.

    :param request: object representing the client's request
    :return: rendered index.html template
    :rtype: HttpResponse
    """

    # Search Form handling
    if request.method == 'POST':
        # Is a post request, so process and send user to tracking url
        form = SearchForm(request.POST)  # Generate form with POST data

        # Check if the data given is valid
        if form.is_valid():
            # redirect to the detail page for tracking
            return HttpResponseRedirect(f"/track/{str(form.cleaned_data.get('tracking_code'))}/")
    else:
        # Generate a blank form due to GET request
        form = SearchForm()

    return render(request, 'PostMaster/index.html', {'searchForm': form})


def tracking_details(request, tracking_code):
    """
    Returns a rendered detail page for tracking a package by tracking code.

    :param request: object representing the client's request
    :param tracking_code: UUID tracking code of searched package
    :type tracking_code: UUID
    :return: rendered trackingDetails.html template
    :rtype: HttpResponse
    """

    # Search Form handling
    if request.method == 'POST':
        # Is a post request, so process and send user to tracking url
        form = SearchForm(request.POST)  # Generate form with POST data

        # Check if the data given is valid
        if form.is_valid():
            # redirect to the detail page for tracking
            return HttpResponseRedirect(f"/track/{str(form.cleaned_data.get('tracking_code'))}/")
    else:
        # Generate a blank form due to GET request
        form = SearchForm()

    tracking_status = "Unknown Status"
    try:
        tracking_result = Tracking.objects.get(tracking_code=tracking_code)
        STATUSES = {x[0]: x[1] for x in tracking_result.STATUS_CHOICES}
        if tracking_result.status in STATUSES:
            tracking_status = STATUSES[tracking_result.status]
    except Tracking.DoesNotExist:
        tracking_result = False

    # Request Context
    context = {
        'tracking_result': tracking_result,
        'tracking_status': tracking_status,
        'searchForm': form,
    }
    return render(request, 'PostMaster/trackingDetails.html', context)


# -------------------- #
#   Public API Views   #
# -------------------- #

def api_ratelimit_error(request, exception):
    """
    Returns 429 Too Many Requests and ratelimited error because user exceeded the API ratelimit.

    :param exception:
    :param request: object representing the client's request
    :return: 429 Too Many Requests + ratelimited error
    :rtype: JsonResponse
    """
    response = {
        'error': 'ratelimited',
        'acceptable_rate': api_ratelimit
    }

    return JsonResponse(response, status=429)


@ratelimit(group='api', key='ip', rate=api_ratelimit, block=True)
def api(request):
    """
    Returns details about the API in JSON API format

    :param request: object representing the client's request
    :return: API details
    :rtype: JsonResponse
    """

    response = {
        'name': 'Western League Post API',
        'version': '1.0.0-alpha'
    }
    return JsonResponse(response)


# Base page for tracking (no UUID provided)
@ratelimit(group='api', key='ip', rate=api_ratelimit, block=True)
def api_tracking(request):
    """
    Returns 421 Misdirected Request and tracking_id_missing error because user visited the page without providing a
    tracking ID.

    :param request: object representing the client's request
    :return: 421 Misdirected Request + tracking_id_missing error
    :rtype: JsonResponse
    """

    response = {
        'error': 'tracking_id_missing'
    }
    # Respond with a 421 (Misdirected Request).
    return JsonResponse(response, status=421)


# Page for displaying details of a tracking code (UUID provided)
@ratelimit(group='api', key='ip', rate=api_ratelimit, block=True)
def api_details(request, tracking_code):
    """
    Returns tracking details about the requested package in JSON API format

    :param request: object representing the client's request
    :param tracking_code: UUID tracking code of searched package
    :type tracking_code: UUID
    :return: package tracking details (or 404 Not Found)
    :rtype: JsonResponse
    """

    try:
        package = Tracking.objects.get(tracking_code=tracking_code)
        status = 200
        package_details = {
            "delivery_address": str(package.package.delivery_address),
            "return_address": str(package.package.return_address),
            "from_nation": str(package.package.from_nation),
            "to_nation": str(package.package.to_nation),
            "date_received": str(package.package.receiving_date),
            "current_status": str(package.status)
        }
    except PostMaster.models.Tracking.DoesNotExist:
        status = 404
        package_details = {
            "error": "package_not_found"
        }

    return JsonResponse(package_details, status=status)
