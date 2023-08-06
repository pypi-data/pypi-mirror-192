from datetime import datetime

from qa_data_manager.data_base_model import SlotsDoctors, ConfirmationCodes, Users, DoctorPatient, Chats, ClinicUser, \
    Clinics, Services


class SlotDoctorTable:
    # Вся строка из таблицы по id слота
    def slot_info_by_id(self, slot_id):
        return SlotsDoctors.select().where(SlotsDoctors.id == slot_id).get()

    # Дата и время начала определенного слота по id
    def start_at_by_id(self, slot_id):
        return datetime.strptime(str(self.slot_info_by_id(slot_id).start_at), "%Y-%m-%d %H:%M:%S")

    # Дата и время начала определенного слота по id
    def slot_info_by_doctor(self, doctor):
        return SlotsDoctors.select().where(SlotsDoctors.doctor == doctor.get("id"))

    # Дата и время начала определенного слота по id
    def first_slot_info_by_list_of_slots_ids(self, slots_ids):
        return SlotsDoctors.select().where(SlotsDoctors.id == slots_ids[0]).get()

    # Дата и время всех слотов на определенный день
    def list_of_slots_start_at_by_day_and_gen_person(self, day, gen_doctor):
        slots_list_bd = []
        slots_bd = SlotsDoctors.select().where(
            (SlotsDoctors.start_at.contains(f"{day}")) & (SlotsDoctors.doctor == gen_doctor.get("id")))
        for s in slots_bd.objects():
            slots_list_bd.append(datetime.strftime((s.start_at), "%H:%M"))
        return slots_list_bd

    # Дата и время всех слотов на определенный день
    def list_of_slots_start_at_by_gen_person(self, gen_doctor):
        slots_list_bd = []
        slots_bd = self.slot_info_by_doctor(gen_doctor)
        for s in slots_bd.objects():
            slots_list_bd.append(datetime.strftime((s.start_at), "%H:%M"))
        return slots_list_bd


class UserTable:
    # Вся строка из таблицы по сгенерированному пользователю
    def info_by_gen_person(self, person):
        return Users.select().where(Users.phone == person.get('phone')).get()

    # Код по сгенерированному пользователю
    def code_by_gen_person(self, person):
        return self.info_by_gen_person(person).code

    # Registration code по сгенерированному пользователю
    def registration_code_by_gen_person(self, person):
        return self.info_by_gen_person(person).registration_code

    # Ссылка на аватарку по сгенерированному пользователю
    def avatar_by_gen_person(self, person):
        return self.info_by_gen_person(person).avatar

    # Кол-во пациентов по номеру телефона (маска + сам номер)
    def count_of_patient_by_mask_and_number(self, mask, patient_phone):
        return Users.select().where((Users.phone == f"{mask}{patient_phone}") & (Users.type == "patient") & (
            Users.deleted_at.is_null())).count()


class ConfirmationCodesTable:
    # Код по пользователю через запрос к БД
    def get_code_by_req_person(self, person):
        return ConfirmationCodes.select().where(ConfirmationCodes.user_id == person.id).get().code

    # Код по сгенерированному пользователю
    def get_code_by_gen_person(self, person):
        return ConfirmationCodes.select().where(ConfirmationCodes.user_id == person.get("id")).get().code


class DoctorPatientTable:
    # Кол-во записей между id двух пользователей через сгенерированного доктора и запрос к БД по пациенту
    def count_of_value_by_gen_doc_req_pat(self, doctor, patient):
        return DoctorPatient.select().where(
            (DoctorPatient.doctor == doctor.get('id')) & (DoctorPatient.patient == patient.id)).count()

    # Кол-во записей между id двух пользователей через сгенерированного доктора и сгенерированного пациента
    def count_of_value_by_gen_doc_gen_pat(self, doctor, patient):
        return DoctorPatient.select().where(
            (DoctorPatient.doctor == doctor.get('id')) & (DoctorPatient.patient == patient.get('id'))).count()


class ChatsTable:
    # Кол-во записей между id двух пользователей через сгенерированного доктора и запрос к БД по пациенту
    def count_of_value_by_gen_doc_req_pat(self, doctor, patient):
        return Chats.select().where(
            (Chats.doctor == doctor.get('id')) & (Chats.patient == patient.id)).count()

    # Кол-во записей между id двух пользователей через сгенерированного доктора и сгенерированного пациента
    def count_of_value_by_gen_doc_gen_pat(self, doctor, patient):
        return Chats.select().where(
            (Chats.doctor == doctor.get('id')) & (Chats.patient == patient.get('id'))).count()


class ClinicUserTable:
    # id клиники по сгенерированному пользователю
    def clinic_id_by_gen_person(self, person):
        return ClinicUser.select().where(ClinicUser.user == person.get("id")).get().clinic


class ClinicTable:
    # Название клиники по id клиники
    def name_by_clinic_id(self, clinic_id):
        return Clinics.select().where(Clinics.id == clinic_id).get().name

    # Название клиники по сгенерированной клинике
    def name_by_gen_clinic(self, gen_clinic):
        return Clinics.select().where(Clinics.id == gen_clinic.get("id")).get().name

    # Город и улица клиники по id клиники
    def address_by_clinic_id(self, clinic_id):
        info = Clinics.select().where(Clinics.id == clinic_id).get()
        return info.city + ", " + info.street

    # Город и улица клиники по сгенерированной клинике
    def address_by_gen_clinic(self, gen_clinic):
        info = Clinics.select().where(Clinics.id == gen_clinic.get("id")).get()
        return info.city + ", " + info.street


class ServicesTable:
    # Деактивация тарифа
    def deactivate_tariff(self, tariff):
        Services.update(active=0).where(Services.id == tariff.get("id")).execute()
