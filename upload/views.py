from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from . import FileObject

from .models import UploadStudent

import pandas as pd
# Create your views here.


def home(request):
	return render(request, 'upload/upload_student.html')


class uploadFile(APIView):
	#parser_classes = (FileUploadParser,)
	parser_classes = (MultiPartParser, FormParser)


	def post(self, request, filename=None, format=None):
		file = request.FILES['file']
		file_obj= FileObject.StudentFile(file)

		final_answer=file_obj.validate_file()

		if(final_answer[0]=="everything correct"):
			UploadStudent.objects.create(file=file)
			db_stored="true"
		else:
			db_stored="false"


		return Response({'validation':final_answer,'db_stored':db_stored})










