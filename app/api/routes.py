# Sample

# from fastapi import APIRouter, HTTPException, Depends
# from app.models.schemas import VideoRequest, DetectionResult
# from app.services.video_service import VideoService
# from app.dependencies.yolo_loader import get_yolo_model
# from app.core.utils import verify_jwt_token
 
# router = APIRouter()
 
# @router.post(
#     "/process_video/",
#     response_model=list[DetectionResult],
#     summary="Process a video for person tracking",
#     description="Processes a video file provided via Azure Blob Storage URL and returns analytics on detected people and their time spent in the video.",
#     tags=["Video Processing"],
# )
# async def process_video(
#     video_request: VideoRequest,
#     token: str = Depends(verify_jwt_token),
#     yolo_model=Depends(get_yolo_model),
# ):
#     """
#     Process a video and track people.
#     - **blob_url**: URL to the video in Azure Blob Storage.
#     - **container_name**: Name of the Azure Blob container.
#     - **blob_name**: Name of the video blob.
#     - **connection_string**: Connection string for Azure Blob Storage.
 
#     Returns a list of people tracked and their time spent.
#     """
#     try:
#         video_service = VideoService(yolo_model)
#         return await video_service.process_video(video_request)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")