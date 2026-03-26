
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# -------------------------------
# #GymManagementSystem #PlansData
# -------------------------------
plans = [
    {"id": 1, "name": "Basic", "duration_months": 1, "price": 29, "includes_classes": False, "includes_trainer": False},
    {"id": 2, "name": "Standard", "duration_months": 3, "price": 79, "includes_classes": True, "includes_trainer": False},
    {"id": 3, "name": "Premium", "duration_months": 6, "price": 149, "includes_classes": True, "includes_trainer": True},
    {"id": 4, "name": "Elite", "duration_months": 12, "price": 299, "includes_classes": True, "includes_trainer": True},
    {"id": 5, "name": "Ultimate", "duration_months": 24, "price": 599, "includes_classes": True, "includes_trainer": True}
]




# -------------------------------
# #HomeAPI - Question 1
# -------------------------------
@app.get("/")
def home():
    return {"message": "Welcome to IronFit Gym"}


# -------------------------------
# #GetPlansAPI #PriceRange - Question 2
# -------------------------------
@app.get("/plans")
def read_plans():
    prices = [plan["price"] for plan in plans]

    return {
        "plans": plans,
        "total": len(plans),
        "price_range": {
            "min_price": min(prices),
            "max_price": max(prices)
        }
    }



# -------------------------------
# #MembershipsAPI # question 4
# -------------------------------

memberships = []
membership_counter = 1


@app.get("/memberships")
def read_memberships():
    return {
        "memberships": memberships,
        "total": len(memberships)
    }
# -------------------------------
# #PlansSummary # Question 5
# -------------------------------
@app.get("/plans/summary")
def read_plans_summary():
    include_classes = sum(1 for p in plans if p["includes_classes"])
    include_trainer = sum(1 for p in plans if p["includes_trainer"])

    cheapest = min(plans, key=lambda x: x["price"])
    expensive = max(plans, key=lambda x: x["price"])

    return {
        "total_plans": len(plans),
        "include_classes": include_classes,
        "include_trainer": include_trainer,
        "cheapest_plan": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "most_expensive_plan": {
            "name": expensive["name"],
            "price": expensive["price"]
        }
    }
    
# -------------------------------
# #InputValidation #Question 6
# -------------------------------
class EnrollRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    plan_id: int = Field(..., gt=0)
    phone: str = Field(..., min_length=10)
    start_month: str = Field(..., min_length=3)
    payment_mode: str = "cash"
    referral_code: str = ""
    
# -------------------------------
# #HelperFunction # Question 7
# -------------------------------
@app.get("/test/calculate-fee")
def test_calculate_fee():
    result1 = calculate_membership_fee(149, 6, "cash")
    result2 = calculate_membership_fee(299, 12, "emi", "REF100")

    return {
        "case_1": result1,
        "case_2": result2
    }
    
def find_plan(plan_id: int):
    for plan in plans:
        if plan["id"] == plan_id:
            return plan
    return None


# calculate membership fee
# question 9 - add referral code field 
def calculate_membership_fee(base_price, duration_months, payment_mode, referral_code=""):
    original_fee = base_price * duration_months

    discount_percent = 0
    if duration_months >= 12:
        discount_percent = 20
    elif duration_months >= 6:
        discount_percent = 10

    duration_discount = (original_fee * discount_percent) / 100
    fee_after_duration = original_fee - duration_discount

    # question 9 - referral code
    referral_discount = 0
    if referral_code.strip() != "":
        referral_discount = (fee_after_duration * 5) / 100

    fee_after_all = fee_after_duration - referral_discount

    processing_fee = 0
    if payment_mode.lower() == "emi":
        processing_fee = 200

    final_fee = fee_after_all + processing_fee

    return {
        "original_fee": original_fee,
        "duration_discount_percent": discount_percent,
        "duration_discount_amount": round(duration_discount, 2),
        "referral_discount_percent": 5 if referral_code.strip() != "" else 0,
        "referral_discount_amount": round(referral_discount, 2),
        "processing_fee": processing_fee,
        "final_fee": round(final_fee, 2)
    }


# -------------------------------
# #Create POST Membership # Question 8
# -------------------------------
@app.post("/memberships")
def create_membership(enroll_request: EnrollRequest):
    global membership_counter

    plan = find_plan(enroll_request.plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    fee_details = calculate_membership_fee(
        plan["price"],
        plan["duration_months"],
        enroll_request.payment_mode,
        enroll_request.referral_code
    )

    membership = {
        "membership_id": membership_counter,
        "member_name": enroll_request.member_name,
        "plan_name": plan["name"],
        "duration_months": plan["duration_months"],
        "monthly_equivalent_cost": round(fee_details["final_fee"] / plan["duration_months"], 2),
        "total_fee": fee_details["final_fee"],
        "status": "active",
        "discount_breakdown": fee_details
    }

    memberships.append(membership)
    membership_counter += 1

    return membership


# -------------------------------
# #FilterAPI # Question 10
# -------------------------------
@app.get("/plans/filter")
def filter_plans(
    max_price: Optional[int] = Query(None),
    max_duration: Optional[int] = Query(None),
    includes_classes: Optional[bool] = Query(None),
    includes_trainer: Optional[bool] = Query(None)
):
    filtered = plans

    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]

    if max_duration is not None:
        filtered = [p for p in filtered if p["duration_months"] <= max_duration]

    if includes_classes is not None:
        filtered = [p for p in filtered if p["includes_classes"] == includes_classes]

    if includes_trainer is not None:
        filtered = [p for p in filtered if p["includes_trainer"] == includes_trainer]

    return {
        "plans": filtered,
        "total": len(filtered)
    }
    

    
# Medium CRUD operations and multi-step workflows Q11–15

# Create NewPlan model: name (min 2), duration_months (gt 0), price (gt 0), 
# includes_classes (bool, default False), includes_trainer (bool, default False). 
# Build POST /plans — reject duplicate names. Return with status 201.

#======================================
# question 11
#=====================================

class NewPlan(BaseModel):
    name: str = Field(..., min_length=2)
    duration_months: int = Field(..., gt=0)
    price: int = Field(..., gt=0)
    includes_classes: bool = False
    includes_trainer: bool = False
    
@app.post("/plans", status_code=201)
def create_plan(new_plan: NewPlan):

    # check duplicate name
    for plan in plans:
        if plan["name"].lower() == new_plan.name.lower():
            raise HTTPException(status_code=400, detail="Plan name already exists")

    # generate new id
    new_id = max(p["id"] for p in plans) + 1 if plans else 1

    plan_data = {
        "id": new_id,
        "name": new_plan.name,
        "duration_months": new_plan.duration_months,
        "price": new_plan.price,
        "includes_classes": new_plan.includes_classes,
        "includes_trainer": new_plan.includes_trainer
    }

    plans.append(plan_data)

    return plan_data              

# Build PUT /plans/{plan_id} with optional query params price (int), 
# includes_classes (bool), includes_trainer (bool). Return 404 if not found.
# Apply only non-None updates.

#======================================
# question 12
#=====================================
from fastapi import Query

# -------------------------------
# #UpdatePlanAPI #PUT
# -------------------------------
@app.put("/plans/{plan_id}")
def update_plan(
    plan_id: int,
    price: int = Query(None),
    includes_classes: bool = Query(None),
    includes_trainer: bool = Query(None)
):

    # find plan
    for plan in plans:
        if plan["id"] == plan_id:

            # update only if value is given
            if price is not None:
                plan["price"] = price

            if includes_classes is not None:
                plan["includes_classes"] = includes_classes

            if includes_trainer is not None:
                plan["includes_trainer"] = includes_trainer

            return plan

    # if not found
    raise HTTPException(status_code=404, detail="Plan not found")

# Build DELETE /plans/{plan_id}. Return 404 if not found.
# Also check if any active memberships exist for this plan — if yes, return an error (cannot delete a plan with active members). Otherwise delete.

#======================================
# question 13 - 
#=====================================
@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int):

    # check if plan exists
    for plan in plans:
        if plan["id"] == plan_id:

            # check active memberships
            for membership in memberships:
                if membership["plan_name"] == plan["name"] and membership["status"] == "active":
                    raise HTTPException(
                        status_code=400,
                        detail="Cannot delete plan with active memberships"
                    )

            # delete plan
            plans.remove(plan)
            return {"message": "Plan deleted successfully"}

    # if plan not found
    raise HTTPException(status_code=404, detail="Plan not found")

#======================================
# question 14
#=====================================
class_bookings = []
class_counter = 1


class ClassBookingRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    class_name: str = Field(..., min_length=2)
    class_date: str = Field(..., min_length=10)


@app.post("/classes/book")
def book_class(booking_request: ClassBookingRequest):
    global class_counter

    # check active membership with classes
    has_access = False

    for membership in memberships:
        if (
            membership["member_name"].lower() == booking_request.member_name.lower()
            and membership["status"] == "active"
        ):
            # find plan
            for plan in plans:
                if plan["name"] == membership["plan_name"] and plan["includes_classes"]:
                    has_access = True
                    break

    if not has_access:
        raise HTTPException(
            status_code=400,
            detail="Member does not have class access"
        )

    # create booking
    booking = {
        "booking_id": class_counter,
        "member_name": booking_request.member_name,
        "class_name": booking_request.class_name,
        "class_date": booking_request.class_date
    }

    class_bookings.append(booking)
    class_counter += 1

    return booking

@app.get("/classes/bookings")
def get_class_bookings():
    return {
        "bookings": class_bookings,
        "total": len(class_bookings)
    }

# Build DELETE /classes/cancel/{booking_id} to cancel a class booking
# Build PUT /memberships/{membership_id}/freeze — change membership status to \'frozen\' (member can pause). 
# Build PUT /memberships/{membership_id}/reactivate — change status back to \'active\'.

#======================================
# question 15
#=====================================

@app.delete("/classes/cancel/{booking_id}")
def cancel_class(booking_id: int):
    for booking in class_bookings:
        if booking["booking_id"] == booking_id:
            class_bookings.remove(booking)
            return {"message": "Class booking cancelled successfully"}

    raise HTTPException(status_code=404, detail="Booking not found")

@app.put("/memberships/{membership_id}/freeze")
def freeze_membership(membership_id: int):  
    for membership in memberships:
        if membership["membership_id"] == membership_id:
            membership["status"] = "frozen"
            return {"message": "Membership frozen successfully"}

    raise HTTPException(status_code=404, detail="Membership not found")         

@app.put("/memberships/{membership_id}/reactivate")
def reactivate_membership(membership_id: int):
    for membership in memberships:
        if membership["membership_id"] == membership_id:
            membership["status"] = "active"
            return {"message": "Membership reactivated successfully"}

    raise HTTPException(status_code=404, detail="Membership not found")

# Hard Search, sort, pagination, and combined logic Q16–20

# Build GET /plans/search with required param keyword (str). 
# Search across name, case-insensitive. 
# Also check if the keyword is \'classes\' or \'trainer\' — return plans that include classes or trainer respectively. Return matches and total_found.

#======================================
# question 16
#=====================================
@app.get("/plans/search")
def search_plans(keyword: str = Query(..., min_length=1)):
    keyword_lower = keyword.lower()
    matches = []

    for plan in plans:
        if (
            keyword_lower in plan["name"].lower() or
            (keyword_lower == "classes" and plan["includes_classes"]) or
            (keyword_lower == "trainer" and plan["includes_trainer"])
        ):
            matches.append(plan)

    return {
        "matches": matches,
        "total_found": len(matches)
    }   
    
# Build GET /plans/sort — allow sort_by: price, name, duration_months. Default sort by price ascending. Validate params. Return sorted list.

#======================================
# question 17
#=====================================
@app.get("/plans/sort")
def sort_plans(
    sort_by: str = Query("price", pattern="^(price|name|duration_months)$"),
    order: str = Query("asc", pattern="^(asc|desc)$")
):
    reverse = order == "desc"

    sorted_plans = sorted(
        plans,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    return {
        "plans": sorted_plans
    }

#======================================
# question 18
#=====================================

# Build GET /plans/page with page (default 1) and limit (default 2). 
# Full pagination with total_pages. Test all pages.
@app.get("/plans/page")
def paginate_plans(
    page: int = Query(1, gt=0),
    limit: int = Query(2, gt=0)
):
    total_plans = len(plans)
    total_pages = (total_plans + limit - 1) // limit

    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")

    start = (page - 1) * limit
    end = start + limit

    return {
        "plans": plans[start:end],
        "total_plans": total_plans,   
        "total_pages": total_pages,
        "current_page": page
    }
    
# Build GET /memberships/search — search by member_name. 
# Build GET /memberships/sort — sort by total_fee or duration_months. 
# Build GET /memberships/page for paginating the memberships list.

#======================================
# question 19
#=====================================

@app.get("/memberships/search")
def search_memberships(member_name: str = Query(..., min_length=1)):
    matches = []

    for membership in memberships:
        if member_name.lower() in membership["member_name"].lower():
            matches.append(membership)

    return {
        "matches": matches,
        "total_found": len(matches)
    }


# #SortMembershipsAPI
@app.get("/memberships/sort")
def sort_memberships(
    sort_by: str = Query("total_fee", pattern="^(total_fee|duration_months)$"),
    order: str = Query("asc", pattern="^(asc|desc)$")
):
    reverse = True if order == "desc" else False

    sorted_memberships = sorted(
        memberships,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    return {
        "memberships": sorted_memberships,
        "sorted_by": sort_by,
        "order": order
    }


# #PaginationMembershipsAPI
@app.get("/memberships/page")
def paginate_memberships(
    page: int = Query(1, gt=0),
    limit: int = Query(2, gt=0)
):
    total_memberships = len(memberships)
    total_pages = (total_memberships + limit - 1) // limit

    if total_memberships == 0:
        return {
            "memberships": [],
            "total_memberships": 0,
            "total_pages": 0,
            "current_page": page
        }

    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")

    start = (page - 1) * limit
    end = start + limit

    return {
        "memberships": memberships[start:end],
        "total_memberships": total_memberships,
        "total_pages": total_pages,
        "current_page": page
    }
    
# Build GET /plans/browse combining: optional keyword, includes_classes filter (bool), includes_trainer filter (bool), sort_by, order, page, limit. 
# Apply in order: keyword → boolean filters → sort → paginate. Return full metadata.

#======================================
# question 20
#=====================================

# #BrowsePlansAPI #SearchFilterSortPaginate
@app.get("/plans/browse")
def browse_plans(
    keyword: str = Query(None),
    includes_classes: bool = Query(None),
    includes_trainer: bool = Query(None),
    sort_by: str = Query("price", pattern="^(price|name|duration_months)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    page: int = Query(1, gt=0),
    limit: int = Query(2, gt=0)
):
    result = plans

    # 1. keyword search
    if keyword is not None and keyword.strip() != "":
        keyword_lower = keyword.lower()
        filtered = []

        for plan in result:
            if (
                keyword_lower in plan["name"].lower()
                or (keyword_lower == "classes" and plan["includes_classes"])
                or (keyword_lower == "trainer" and plan["includes_trainer"])
            ):
                filtered.append(plan)

        result = filtered

    # 2. boolean filters
    if includes_classes is not None:
        result = [plan for plan in result if plan["includes_classes"] == includes_classes]

    if includes_trainer is not None:
        result = [plan for plan in result if plan["includes_trainer"] == includes_trainer]

    # 3. sorting
    reverse = order == "desc"
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # 4. pagination
    total_found = len(result)
    total_pages = (total_found + limit - 1) // limit if total_found > 0 else 0

    if total_found > 0 and page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found")

    start = (page - 1) * limit
    end = start + limit
    paginated_result = result[start:end]

    return {
        "plans": paginated_result,
        "metadata": {
            "keyword": keyword,
            "includes_classes": includes_classes,
            "includes_trainer": includes_trainer,
            "sort_by": sort_by,
            "order": order,
            "page": page,
            "limit": limit,
            "total_found": total_found,
            "total_pages": total_pages
        }
    }
    
# -------------------------------
# #PlanByID Question - 3
# -------------------------------
@app.get("/plans/{plan_id}")
def read_plan(plan_id: int):
    for plan in plans:
        if plan["id"] == plan_id:
            return plan

    raise HTTPException(status_code=404, detail="Plan not found")