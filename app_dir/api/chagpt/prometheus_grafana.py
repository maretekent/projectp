from django_prometheus.views import ExportPrometheusMetricsView

urlpatterns = [
    ...
    path("metrics/", ExportPrometheusMetricsView.as_view()),
    ...
]


