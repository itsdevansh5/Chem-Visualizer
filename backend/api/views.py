import io
import pandas as pd
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Dataset
from .serializers import DatasetSerializer
from reportlab.pdfgen import canvas


# -----------------------------
# Utility function: compute stats
# -----------------------------
def compute_summary(df: pd.DataFrame):
    total_count = len(df)

    numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
    averages = {}

    # convert numeric columns safely
    for col in numeric_cols:
        if col in df.columns:
            series = pd.to_numeric(df[col], errors='coerce').dropna()
            averages[col] = float(series.mean()) if len(series) > 0 else None
        else:
            averages[col] = None

    # Equipment type distribution
    type_distribution = (
        df['Type'].value_counts().to_dict()
        if 'Type' in df.columns
        else {}
    )

    return {
        'total_count': int(total_count),
        'averages': averages,
        'type_distribution': type_distribution,
    }


# -----------------------------
# Upload CSV Endpoint
# -----------------------------
class UploadCSV(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({'error': 'No file uploaded!'}, status=400)

        name = request.data.get('name') or csv_file.name

        # Parse CSV using pandas
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return Response({'error': 'Invalid CSV: ' + str(e)}, status=400)

        summary = compute_summary(df)
        preview = df.head(10).to_csv(index=False)

        # Reset file pointer before saving to model
        csv_file.seek(0)

        dataset = Dataset.objects.create(
            name=name,
            file=csv_file,
            summary=summary,
            preview_csv=preview
        )

        # Keep only last 5 datasets
        all_data = Dataset.objects.all().order_by('-uploaded_at')
        for old in all_data[5:]:
            if old.file:
                old.file.delete(save=False)
            old.delete()

        serializer = DatasetSerializer(dataset)
        return Response(serializer.data, status=201)


# -----------------------------
# History: return last 5 uploads
# -----------------------------
class History(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Dataset.objects.all().order_by('-uploaded_at')[:5]
        serializer = DatasetSerializer(qs, many=True)
        return Response(serializer.data)


# -----------------------------
# Summary detail
# -----------------------------
class SummaryDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            ds = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

        serializer = DatasetSerializer(ds)
        return Response(serializer.data)


# -----------------------------
# PDF Report Generator
# -----------------------------
class GeneratePDF(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            ds = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

        # Create PDF in memory
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)

        p.setFont("Helvetica", 14)
        p.drawString(50, 800, f"Dataset Report: {ds.name}")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, 780, f"Uploaded at: {ds.uploaded_at}")

        summary = ds.summary
        y = 750

        p.drawString(50, y, f"Total Records: {summary['total_count']}")
        y -= 30

        p.drawString(50, y, "Averages:")
        y -= 20
        for k, v in summary['averages'].items():
            p.drawString(70, y, f"{k}: {v}")
            y -= 20

        y -= 10
        p.drawString(50, y, "Type Distribution:")
        y -= 20
        for t, c in summary['type_distribution'].items():
            p.drawString(70, y, f"{t}: {c}")
            y -= 20

        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
