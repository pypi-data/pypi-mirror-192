# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         15/02/23 8:49
# Project:      CFHL Transactional Backend
# Module Name:  sync_users
# Description:
# ****************************************************************
from core import celery_app
from django.contrib.auth import get_user_model
from oasis.models import Client
from typing import Any


@celery_app.task(bind=True)
def task_sync_users(app: Any):
    """
    Task to get user state, email and other variables to user table.
    :return: None
    """

    user_model = get_user_model()
    user_qs = user_model.objects.all()
    for user in user_qs:
        if hasattr(user, "profile"):
            document_id = user.profile.document_id
            try:
                oasis_customer = Client.objects.get_by_pk(pk=document_id).get()
                if user.is_active != (oasis_customer.state == "A"):
                    user.is_active = (oasis_customer.state == "A")

                if user.email != oasis_customer.main_email:
                    user.email = oasis_customer.main_email
            except Client.DoesNotExist:
                user.is_active = False
            except Exception as exc:
                pass
            else:
                user.save()


