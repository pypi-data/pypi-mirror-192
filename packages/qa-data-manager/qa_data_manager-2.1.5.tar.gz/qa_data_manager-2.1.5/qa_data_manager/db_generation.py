from qa_data_manager.bind_clinic_user import BindClinicUser
from qa_data_manager.bind_doctor_patient import BindDoctorPatient
from qa_data_manager.bind_doctor_specialties import BindDoctorSpecialties
from qa_data_manager.clinic import GenerateClinic
from qa_data_manager.consultation import GenerateConsultation
from qa_data_manager.patient_problem import GeneratePatientProblem
from qa_data_manager.patient_problem_discomfort import GeneratePatientProblemDiscomfort
from qa_data_manager.patient_problem_slot_patient import GeneratePatientProblemSlotPatient
from qa_data_manager.service import GenerateService
from qa_data_manager.slot_doctor_patient import GenerateSlotDoctorPatient
from qa_data_manager.tracks import GenerateTracks
from qa_data_manager.user import GenerateUser


class ConsultationGenerate:

    def completed_offline(self, slots_ids, patient, tariff_offline, doctor, slot_info):
        # slots_ids - список нарезанных слотов доктора
        # slot_info - строка информации по слоту из таблицы Slot_doctor_table
        # Генерация завершенной консультации между доктором и пациентом
        slot_doc_pat = GenerateSlotDoctorPatient(slots_ids[0], patient,
                                                 tariff_offline).with_patient_source().with_offline_type().with_completed_status().generate()
        consultation = GenerateConsultation(doctor, patient, tariff_offline, slot_info,
                                            slot_doc_pat.get(
                                                'id')).with_type_offline().with_status_completed().generate()
        # Генерация проблемы
        problem = GeneratePatientProblem(patient).generate()
        GenerateTracks(problem).with_status_second_opinion().generate()
        # Генерация уровня дискомфорта к консультации
        GeneratePatientProblemDiscomfort(consultation, problem).generate()
        # Генерация связи между проблемой и консультацией
        GeneratePatientProblemSlotPatient(problem, tariff_offline, slot_doc_pat).generate()

    def completed_online(self, slots_ids, patient, tariff_video, doctor, slot_info):
        # slots_ids - список нарезанных слотов доктора
        # slot_info - строка информации по слоту из таблицы Slot_doctor_table
        # Генерация завершенной консультации между доктором и пациентом
        slot_doc_pat = GenerateSlotDoctorPatient(slots_ids[0], patient,
                                                 tariff_video).with_patient_source().with_online_type().with_completed_status().generate()
        consultation = GenerateConsultation(doctor, patient, tariff_video, slot_info,
                                            slot_doc_pat.get('id')).with_status_completed().generate()
        # Генерация проблемы
        problem = GeneratePatientProblem(patient).generate()
        GenerateTracks(problem).with_status_second_opinion().generate()
        # Генерация уровня дискомфорта к консультации
        GeneratePatientProblemDiscomfort(consultation, problem).generate()
        # Генерация связи между проблемой и консультацией
        GeneratePatientProblemSlotPatient(problem, tariff_video, slot_doc_pat).generate()

    # Генерация записи на слот для проверки ошибочной записи на занятый слот
    def record_on_slot(self, slot_id, patient, tariff):
        GenerateSlotDoctorPatient(slot_id, patient, tariff).with_online_type().generate()


class PreconditionGenerate:
    # Генерация второй клиники и связи с ней, доктора и связи с ним.
    def second_clinic_and_doctor(self, patient):
        # Генерация новой клиники
        new_clinic = GenerateClinic().generate()
        # Генерация связи пациента и новой клиники
        BindClinicUser(patient).with_clinic(new_clinic.get("id")).generate()
        # Генерация доктора
        doctor2 = GenerateUser().doctor().is_activated().with_clinic(
            new_clinic).with_self_appointment().with_primary_acceptance().generate()
        # Генерация специализации доктора
        BindDoctorSpecialties(doctor2).generate()
        # Генерация тарифа для видео
        GenerateService(doctor2).is_active().with_price(10).is_default().generate()
        # Генерация связи между доктором и пациентом
        BindDoctorPatient(doctor2, patient).generate()
        return new_clinic

    def gen_3_tariff(self, gen_doctor):
        # Генерация двух тарифов для чата
        tariff_chat = GenerateService(gen_doctor).with_chat_service_type().is_active().with_price(
            0).is_default().with_duration(5).generate()
        tariff_chat2 = GenerateService(gen_doctor).with_chat_service_type().is_active().with_price(10).with_duration(
            10).generate()
        # Генерация списка "Названия тарифов для чата"
        chat_names_list = []
        chat_names_list.append(tariff_chat.get("name"))
        chat_names_list.append(tariff_chat2.get("name"))
        # Генерация списка "Описания тарифов для чата"
        chat_desc_list = []
        chat_desc_list.append(tariff_chat.get("description"))
        chat_desc_list.append(tariff_chat2.get("description"))
        # Генерация двух тарифов для видеоконсультации
        tariff_video = GenerateService(gen_doctor).is_active().with_price(0).is_default().with_duration(5).generate()
        tariff_video2 = GenerateService(gen_doctor).is_active().with_price(10).with_duration(10).generate()
        # Генерация списка "Названия тарифов для видеоконсультации"
        video_names_list = []
        video_names_list.append(tariff_video.get("name"))
        video_names_list.append(tariff_video2.get("name"))
        # Генерация списка "Описания тарифов для видеоконсультации"
        video_desc_list = []
        video_desc_list.append(tariff_video.get("description"))
        video_desc_list.append(tariff_video2.get("description"))
        # Генерация двух тарифов для приема в клинике
        tariff_offline = GenerateService(gen_doctor).with_offline_service_type().is_active().with_price(
            0).is_default().with_duration(10).with_duration(5).generate()
        tariff_offline2 = GenerateService(gen_doctor).with_offline_service_type().is_active().with_price(
            10).with_duration(
            10).generate()
        # Генерация списка "Названия тарифов для приема в клинике"
        offline_names_list = []
        offline_names_list.append(tariff_offline.get("name"))
        offline_names_list.append(tariff_offline2.get("name"))
        # Генерация списка "Описания тарифов для приема в клинике"
        offline_desc_list = []
        offline_desc_list.append(tariff_offline.get("description"))
        offline_desc_list.append(tariff_offline2.get("description"))
        # Создания списка продолжительностей тарифов
        duration_list = ["Длительность 5 мин", "Длительность 10 мин"]
        # Создания списка стоимости тарифов
        price_list = ["0 ₽", "10 ₽"]
        info_dict = {'chat_names_list': chat_names_list, 'chat_desc_list': chat_desc_list,
                     'video_names_list': video_names_list, 'video_desc_list': video_desc_list,
                     'offline_names_list': offline_names_list, 'offline_desc_list': offline_desc_list,
                     'tariff_video': tariff_video, 'duration_list': duration_list, 'price_list': price_list}
        return info_dict
