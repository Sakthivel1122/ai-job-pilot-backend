from app.schemas.user import JobApplicationRequest, JobApplicationResponse
from app.utils.response import response
from app.models.user import JobApplication, User
from fastapi.encoders import jsonable_encoder
from beanie import PydanticObjectId
from bson import ObjectId
from typing import Optional
from beanie.operators import And
from math import ceil

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

            res = JobApplicationResponse(**jsonable_encoder(job_application))
            return response(jsonable_encoder(res), "Updated Successfully", 200)
        else:
            job_data = data.model_dump(exclude_none=True)
            job_application = JobApplication(**job_data, user=user.id)
            await job_application.insert()
            data = jsonable_encoder(job_application)
            return response(data, "Created Successfully!", 200)
    except Exception as e:
        return response(None, f"Failed to create job application", 400)

async def get_all_job_application(
    user: User,
    status: Optional[str],
    page: int,
    limit: int,
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
    except Exception:
        return response(data, "success", 200)

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
