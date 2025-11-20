from app.schemas.user import JobApplicationRequest, JobApplicationResponse
from app.utils.response import response
from app.models.user import JobApplication, User
from fastapi.encoders import jsonable_encoder
from beanie import PydanticObjectId
from bson import ObjectId
from typing import Optional
from beanie.operators import And
from math import ceil
from datetime import datetime

async def create_update_job_application(data: JobApplicationRequest, user: User):
    try:
        if data.id is not None:
            job_application = await JobApplication.find_one(JobApplication.id == PydanticObjectId(data.id), JobApplication.deleted_at == None)

            if not job_application:
                return response(None, "Job Application Not Found", 400)

            update_data = data.model_dump(exclude_none=True, exclude={"id"})
            for field, value in update_data.items():
                setattr(job_application, field, value)
            await job_application.save()

            job_application.updated_at = datetime.utcnow()
            update_dict = job_application.model_dump(exclude_none=True)
            collection = JobApplication.get_motor_collection()
            
            result = await collection.update_one(
                {"_id": job_application.id},
                {"$set": update_dict}
            )
            updated_doc = await collection.find_one({"_id": job_application.id})
            update_dict["_id"] = str(updated_doc["_id"])
            return response(jsonable_encoder(update_dict), "Updated Successfully", 200)
        else:
             # ----- CREATE -----
            job_data = data.model_dump(exclude_none=True)

            # ensure user.id is BSON ObjectId
            job_data["user"] = PydanticObjectId(str(user.id))
            job_data["created_at"] = datetime.utcnow()
            job_data["updated_at"] = datetime.utcnow()

            # insert directly using Motor collection
            collection = JobApplication.get_motor_collection()
            result = await collection.insert_one(job_data)

            # attach _id for response
            job_data["_id"] = str(result.inserted_id)
            job_data["user"] = str(job_data["user"])

            return response(jsonable_encoder(job_data), "Created Successfully!", 200)
    except Exception as e:
        return response(None, f"Failed to create job application {str(e)}", 400)

async def get_all_job_application(
    user: User,
    page: int,
    limit: int,
    status: Optional[str] = None
):
    try:
        filters = [
            JobApplication.user == ObjectId(user.id),
            JobApplication.deleted_at == None
        ]

        if status:
            filters.append(JobApplication.status == status)

        skip = (page - 1) * limit

        query = JobApplication.find(And(*filters))

        total_records = await query.count()

        job_applications = (
            await query
            .sort("-created_at")
            .project(JobApplicationResponse)
            .skip(skip)
            .limit(limit)
            .to_list()
        )
        data = jsonable_encoder(job_applications)

        result = {
            'data': data,
            'current_page_no': page,
            'total_records': total_records
        }
        return response(result, "Retrieved Successfully", 200)
    except Exception as e:
        return response(None, f"Error: {str(e)}", 400)

async def get_dashboard_data(current_user: User):
    from app.models.user import JobApplication
    from bson import ObjectId

    user_id = ObjectId(current_user.id)

    total = await JobApplication.find(
        JobApplication.user == user_id,
        JobApplication.deleted_at == None
    ).count()

    applied = await JobApplication.find(
        JobApplication.user == user_id,
        JobApplication.status == "applied",
        JobApplication.deleted_at == None
    ).count()

    # interviews = await JobApplication.find(
    #     JobApplication.user == user_id,
    #     JobApplication.status.in_(["interview_scheduled", "interviewing"]),
    #     JobApplication.deleted_at == None
    # ).count()

    # interviews = await JobApplication.find_many(
    # lambda j: j.user == user_id and j.status in ["interview_scheduled", "interviewing"] and j.deleted_at is None
    # ).to_list()

    # interviews_count = len(interviews)

    interviews = await JobApplication.find({
        "user": user_id,
        "status": {"$in": ["interview_scheduled", "interviewing"]},
        "deleted_at": None
    }).count()

    offers = await JobApplication.find(
        JobApplication.user == user_id,
        JobApplication.status == "selected",
        JobApplication.deleted_at == None
    ).count()

    data = {
        "total_application_count": total,
        "applied_count": applied,
        "interview_count": interviews,
        "offer_count": offers
    }

    return response(data, "Dashboard data fetched", 200)
