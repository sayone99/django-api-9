from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import PostSerializer
from .models import Post

# 1) PostList : 게시글 전체 목록 조회 요청, 게시글 작성 요청 처리
class PostList(APIView):
    # 1-1) GET 요청 : 게시글 전체 목록 조회 요청
    def get(self, request):
        posts = Post.objects.all() #쿼리셋 형태니까 시리얼라이즈로 JSON형태로 바꿔야함

        serializer = PostSerializer(posts, many=True) # 여러개의 객체를 시리얼라이즈하려면 many=True를 설정해야함
        return Response(serializer.data)

    # 1-2) POST 요청 : 게시글 작성 요청
    def post(self, request):
        serializer = PostSerializer(data=request.data) # request.data는 입력받은 데이터
        
        if serializer.is_valid(): #입력받은 값의 유효성 검사
            serializer.save() #입력받은 데이터로 게시글 객체 저장 : 장고 모델폼이랑 비슷하죠?
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 게시글 객체 생성이니까 201 코드 보내기
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 입력값이 유효하지 않다면 400 잘못된 요청 코드 보내기


# 2) PostDetail : 게시글 상세보기 페이지 보여주기 -> GET 요청
class PostDetail(APIView):
    # 게시글 객체 가져오는 함수 따로 빼둠! 나중을 위해
    def get_object(self, postId): # postId는 urls.py에서 작성한 <int:postId>랑 같은 변수명으로 써야 오류가 안납니다.
        try:
            #id 값과 일치하는 게시글 객체가 존재하면 반환
            return Post.objects.get(pk=postId)
        except Post.DoesNotExist: #게시글 객체가 존재하지 않으면 -> 404 존재하지 않는 페이지 요청 코드 보내기
            raise Http404
    
    # 2-1) GET 요청 : 특정 게시글 조회 요청
    def get(self, request, postId, format=None):
        post = self.get_object(postId)
        serializer = PostSerializer(post)
        return Response(serializer.data)