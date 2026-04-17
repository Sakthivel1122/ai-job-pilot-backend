from app.models.user import User, JobApplication, Resume
from app.utils.response import response
from app.constants.job_application import JOBAPPLICATION_STATUS_LIST
from app.models.auth_log import AuthLog
from app.models.user import User
from fastapi.encoders import jsonable_encoder
from beanie import PydanticObjectId
from typing import Optional
import re

async def admin_dashboard_api_service():
    try:
        total_user_count = await User.find(User.deleted_at == None, User.role == "user").count()
        job_application_count = await JobApplication.find(JobApplication.deleted_at == None).count()
        resume_count = await Resume.find(Resume.deleted_at == None).count()
        pipeline = [
            {"$match": {"deleted_at": None}},
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1}
                }
            }
        ]
        result = await JobApplication.aggregate(pipeline).to_list()
        # Convert result into a nice dict
        status_counts = {status: 0 for status in JOBAPPLICATION_STATUS_LIST}

        for item in result:
            status_counts[item["_id"]] = item["count"]
        
        auth_logs = await AuthLog.find()\
            .sort(-AuthLog.created_at)\
            .limit(5)\
            .to_list()
        response_obj = {
            'total_user_count': total_user_count,
            'job_application_count': job_application_count,
            'resumes_analyzed_count': resume_count,
            'job_application_status_counts': status_counts,
            'auth_logs': jsonable_encoder(auth_logs)
        }
        return response(response_obj, "Retrieved Successfully!", 200)
    except Exception as e:
        return response({'error': str(e)}, "Failed to retrieve data!", 400)

async def admin_get_users_api_service(
    page: int,
    limit: int,
    search_text: Optional[str] = None
):
    try:
        skip = (page - 1) * limit

        # Base filter: not deleted users
        filters = [User.deleted_at == None, User.role == "user"]

        # Optional search filter (case-insensitive)
        if search_text and search_text.strip():
            regex = re.compile(re.escape(search_text.strip()), re.IGNORECASE)

            filters.append({
                "$or": [
                    {"username": {"$regex": regex}},
                    {"email": {"$regex": regex}},
                ]
            })

        # Count total records
        total_records = await User.find(*filters).count()

        # Fetch paginated users
        item_list = (
            await User.find(*filters)
            .sort("-updated_at")
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        items = jsonable_encoder(item_list)

        result = {
            "items": items,
            "page": page,
            "limit": limit,
            "total_records": total_records,
        }

        return response(result, "Retrieved Successfully", 200)

    except Exception as e:
        return response({"error": str(e)}, "Failed to retrieve", 400)


async def admin_get_job_application_list_api_service(
    user_id: str,
    page: int,
    limit: int
):
    try:
        skip = (page - 1) * limit
        total_records = await JobApplication.find(JobApplication.user == PydanticObjectId(user_id), JobApplication.deleted_at == None).count()
        item_list = await JobApplication.find(JobApplication.user == PydanticObjectId(user_id), JobApplication.deleted_at == None)\
            .sort("-updated_at")\
            .skip(skip)\
            .limit(limit)\
            .to_list()
        items = jsonable_encoder(item_list)
        
        result = {
            'items': items,
            'page': page,
            'limit': limit,
            'total_records': total_records
        }
        
        return response(result, "Retrieved Successfully", 200)
    
    except Exception as e:
        return response({'error': str(e)}, "Failed to retrieve", 400)

async def admin_get_resume_list_api_service(
    user_id: str,
    page: int,
    limit: int
):
    try:
        skip = (page - 1) * limit
        total_records = await Resume.find(Resume.user == PydanticObjectId(user_id), Resume.deleted_at == None).count()
        item_list = await Resume.find(Resume.user == PydanticObjectId(user_id), Resume.deleted_at == None)\
            .sort("-updated_at")\
            .skip(skip)\
            .limit(limit)\
            .to_list()
        items = jsonable_encoder(item_list)
        
        result = {
            'items': items,
            'page': page,
            'limit': limit,
            'total_records': total_records
        }
        
        return response(result, "Retrieved Successfully", 200)
    
    except Exception as e:
        return response({'error': str(e)}, "Failed to retrieve", 400)

async def admin_get_job_application_details_api_service(
    user_id: str,
    job_application_id: str,
):
    try:
        job_application_details = await JobApplication.find_one(
            JobApplication.user == PydanticObjectId(user_id),
            JobApplication.deleted_at == None,
            JobApplication.id == PydanticObjectId(job_application_id)
        )
        job_application = jsonable_encoder(job_application_details)
        
        return response(job_application, "Retrieved Successfully", 200)
    
    except Exception as e:
        return response({'error': str(e)}, "Failed to retrieve", 400)
