# @router.post("/matching/hospitals")
# async def match_hospitals(
#     query: MatchingQuery,
#     current_user: User = Depends(get_current_patient),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Geospatial query for nearby hospitals
#     pass