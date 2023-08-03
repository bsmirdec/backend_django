PERMISSIONS_BY_POSITION = {
    "administrator": {
        "employee_create_object": True,
        "employee_view_list": True,
        "employee_retrieve_object": True,
        "employee_update_object": True,
        "employee_delete_object": True,
        "worksite_create_object": True,
        "worksite_view_list": True,
        "worksite_retrieve_object": True,
        "worksite_update_object": True,
        "worksite_delete_object": True,
        "worksiteemployee_create_object": True,
        "worksiteemployee_view_list": True,
        "worksiteemployee_retrieve_object": True,
        "worksiteemployee_update_object": True,
        "worksiteemployee_delete_object": True,
    },
    "director": {
        "employee_create_object": False,
        "employee_view_list": True,
        "employee_retrieve_object": True,
        "employee_update_object": True,
        "employee_delete_object": False,
        "worksite_create_object": True,
        "worksite_view_list": True,
        "worksite_retrieve_object": True,
        "worksite_update_object": True,
        "worksite_delete_object": False,
        "worksiteemployee_create_object": True,
        "worksiteemployee_view_list": True,
        "worksiteemployee_retrieve_object": True,
        "worksiteemployee_update_object": True,
        "worksiteemployee_delete_object": True,
    },
    "studies": {
        "employee_create_object": False,
        "employee_view_list": True,
        "employee_retrieve_object": True,
        "employee_update_object": True,
        "employee_delete_object": False,
        "worksite_create_object": True,
        "worksite_view_list": True,
        "worksite_retrieve_object": True,
        "worksite_update_object": True,
        "worksite_delete_object": True,
        "worksiteemployee_create_object": True,
        "worksiteemployee_view_list": True,
        "worksiteemployee_retrieve_object": True,
        "worksiteemployee_update_object": True,
        "worksiteemployee_delete_object": True,
    },
    "site_director": {
        "employee_create_object": False,
        "employee_view_list": True,
        "employee_retrieve_object": True,
        "employee_update_object": True,
        "employee_delete_object": False,
        "worksite_create_object": False,
        "worksite_view_list": True,
        "worksite_retrieve_object": True,
        "worksite_update_object": True,
        "worksite_delete_object": False,
        "worksiteemployee_create_object": True,
        "worksiteemployee_view_list": True,
        "worksiteemployee_retrieve_object": True,
        "worksiteemployee_update_object": True,
        "worksiteemployee_delete_object": True,
    },
    "site_supervisor": {
        "employee_create_object": False,
        "employee_view_list": True,
        "employee_retrieve_object": True,
        "employee_update_object": True,
        "employee_delete_object": False,
        "worksite_create_object": False,
        "worksite_view_list": True,
        "worksite_retrieve_object": True,
        "worksite_update_object": True,
        "worksite_delete_object": False,
        "worksiteemployee_create_object": False,
        "worksiteemployee_view_list": True,
        "worksiteemployee_retrieve_object": True,
        "worksiteemployee_update_object": False,
        "worksiteemployee_delete_object": False,
    },
    "site_foreman": {
        "employee_create_object": False,
        "employee_view_list": False,
        "employee_retrieve_object": True,
        "employee_update_object": True,
        "employee_delete_object": False,
        "worksite_create_object": False,
        "worksite_view_list": False,
        "worksite_retrieve_object": True,
        "worksite_update_object": False,
        "worksite_delete_object": False,
        "worksiteemployee_create_object": False,
        "worksiteemployee_view_list": False,
        "worksiteemployee_retrieve_object": True,
        "worksiteemployee_update_object": False,
        "worksiteemployee_delete_object": False,
    },
}
