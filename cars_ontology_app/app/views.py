from django.shortcuts import render
from .services.sparql_queries import (
    fetch_all_manufacturers,
    fetch_all_model_version_types,
    fetch_all_models,
    fetch_all_engine_types,
    fetch_all_transmission_types,
    fetch_filtered_listings,
    get_price_range,
)


def home(request):
    brand = request.GET.get("brand")
    model = request.GET.get("model")
    engine = request.GET.get("engine")
    transmission = request.GET.get("transmission")
    model_version_type = request.GET.get("model_version_type")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    car_state = request.GET.get("car_state")

    # Convert min_price and max_price to integers if they are not None
    if min_price:
        min_price = int(min_price)
    if max_price:
        max_price = int(max_price)

    listings = fetch_filtered_listings(
        brand,
        model,
        engine,
        transmission,
        model_version_type,
        min_price,
        max_price,
        car_state,
    )
    manufacturers = fetch_all_manufacturers()
    models = fetch_all_models()
    engine_types = fetch_all_engine_types()
    transmission_types = fetch_all_transmission_types()
    model_version_types = fetch_all_model_version_types()
    min_price_range, max_price_range = get_price_range()

    context = {
        "listings": listings,
        "manufacturers": manufacturers,
        "models": models,
        "engine_types": engine_types,
        "transmission_types": transmission_types,
        "model_version_types": model_version_types,
        "min_price_range": min_price_range,
        "max_price_range": max_price_range,
        "car_state": car_state,
    }
    return render(request, "app/home.html", context)
