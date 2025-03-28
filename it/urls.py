from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from it import views
from it import views_login
from it import api_details
from it import change_password
from it import export_tracker
from it import pending_invoice
from it import deleted_invoice_details as delx
from it import apj_template as apj
from it import clearlake_template as ck
from it import shell_template as sh
from it import mail_format as mf
from it import vessel_template as vt
from it import boss_tracker as btr
from it import chm_tracker as ctr
from it import inr_tracker as inr
from it import cost_per_route as cpr
from it import invoice_no as i
from it import summary_report as sr
# from it import other_invoice as ot
from it import boss_export as eb
from it import inr_export as ei
from it import invoice_entry as ie
from it import json_data as jsx
from it import connection as conn
from it import upload_excel as ue
from it import invoice_raise_summary as rs
from it import front_api as fpi
from it import export_summary_report as esr
from it import export_dsr as dsrx
# from it import gen_invoice as g
from it import upload_files as uf
from it import view_payment as vpx

from it import master_inw as miv
from it import bnk_statement as bst
from it import bank_name as bnx
from it import other_bnk_statement as obs
from it import payment_advice as pa
from it import pid_advice as pid
from it import single_data as ds
from it import get_fetch_api as gfa
from it import get_client_api as gca
from it import export_invoice_summary as eis
from it import reconciliation as rec
from it import client_json as cj
from it import get_account_tab as gat
from it import update_address_details as uad
from it import monthly_summary as ms
from it import other_invoice_template as oit
from it import account_json as acc
from it import reconciliation_inr as rnr
from it import home_page as hg
from it import chm_invoice_template as cit
from it import chm_entry as ce

#from it import other_data as od




urlpatterns = patterns('',	
	url(r'^dashboard/', views.dashboard, name = 'dashboard'),
	url(r'^index/', views.index, name = 'index'),	
	# for CHM
	# url(r'^fetching_data_from_api/', views.fetching_data_from_api, name = 'fetching_data_from_api'),	
	url(r'^welcome/', views.welcome, name = 'welcome'),	
	url(r'^saving_fetching_data/', views.saving_fetching_data, name = 'saving_fetching_data'),
	
	#url(r'^update_client_details/', views.update_client_details, name = 'update_client_details'),
	url(r'^view_client/', views.view_client, name = 'view_client'),
	url(r'^load_client/', views.load_client, name = 'load_client'),
	url(r'^view_chm_vessel/', views.view_chm_vessel, name = 'view_chm_vessel'),
	url(r'^vessel_details/', views.vessel_details, name = 'vessel_details'),	
	url(r'^load_fetching_data/', views.load_fetching_data, name = 'load_fetching_data'),	
	
	#url(r'^get_ship_list/', views.get_ship_list, name = 'get_ship_list'),	
	url(r'^load_for_invoice_details/', views.load_for_invoice_details, name = 'load_for_invoice_details'),	
	url(r'^submit_invoice_details/', views.submit_invoice_details, name = 'submit_invoice_details'),	
	url(r'^select_price_type/', views.select_price_type, name = 'select_price_type'),
	url(r'^vaild_invoice_details/', views.vaild_invoice_details, name = 'vaild_invoice_details'),
	url(r'^view_chm_tracker/', views.view_chm_tracker, name = 'view_chm_tracker'),
	url(r'^update_ship_address/', views.update_ship_address, name = 'update_ship_address'),
	url(r'^view_ship_address/', views.view_ship_address, name = 'view_ship_address'),
	url(r'^select_ship_address/', views.select_ship_address, name = 'select_ship_address'),
	url(r'^paid_invoice_details/', views.paid_invoice_details, name = 'paid_invoice_details'),
	url(r'^getting_invoice_id/', views.getting_invoice_id, name = 'getting_invoice_id'),
	url(r'^payment_invoice/', views.payment_invoice, name = 'payment_invoice'),
	url(r'^view_invoice_template/', views.view_invoice_template, name = 'view_invoice_template'),
	url(r'^view_combined_tracker/', views.view_combined_tracker, name = 'view_combined_tracker'),	
	url(r'^combined_tracker/', views.combined_tracker, name = 'combined_tracker'),	
	
	# url(r'^get_invoice_template/', views.get_invoice_template, name = 'get_invoice_template'),
	url(r'^combined_vessel_details/', views.combined_vessel_details, name = 'combined_vessel_details'),
	url(r'^submit_dsr_invoice/', views.submit_dsr_invoice, name = 'submit_dsr_invoice'),
	url(r'^generate_invoice_pdf/', views.generate_invoice_pdf, name = 'generate_invoice_pdf'),
	url(r'^single_generate_invoice_pdf/', views.single_generate_invoice_pdf, name = 'single_generate_invoice_pdf'),
	url(r'^chm_generate_invoice_pdf/', views.chm_generate_invoice_pdf, name = 'chm_generate_invoice_pdf'),
	url(r'^payment_list/', views.payment_list, name = 'payment_list'),
	url(r'^master_log_tracker/', views.master_log_tracker, name = 'master_log_tracker'),
	url(r'^paid_invoice_list/', views.paid_invoice_list, name = 'paid_invoice_list'),
		
	# for BOSS
	url(r'^fetching_get_api_boss/', views.fetching_get_api_boss, name = 'fetching_get_api_boss'),
	url(r'^fetch_boss/', views.fetch_boss, name = 'fetch_boss'),
	url(r'^view_boss_client/', views.view_boss_client, name = 'view_boss_client'),
	
	#url(r'^load_boss_client/', views.load_boss_client, name = 'load_boss_client'),
	url(r'^saving_boss_fetching_data/', views.saving_boss_fetching_data, name = 'saving_boss_fetching_data'),
	url(r'^update_boss_client_details/', views.update_boss_client_details, name = 'update_boss_client_details'),
	url(r'^view_boss_vessel/', views.view_boss_vessel, name = 'view_boss_vessel'),
	url(r'^submit_invoice_for_boss/', views.submit_invoice_for_boss, name = 'submit_invoice_for_boss'),
	url(r'^selected_vessel_details/', views.selected_vessel_details, name = 'selected_vessel_details'),	
	url(r'^submit_invoice_boss/', views.submit_invoice_boss, name = 'submit_invoice_boss'),	
	url(r'^vaild_boss_invoice_details/', views.vaild_boss_invoice_details, name = 'vaild_boss_invoice_details'),
	
	url(r'^selected_client_boss/', views.selected_client_boss, name = 'selected_client_boss'),	
	url(r'^using_date_select_boss_details/', views.using_date_select_boss_details, name = 'using_date_select_boss_details'),	
	url(r'^submit_selected_boss/', views.submit_selected_boss, name = 'submit_selected_boss'),
	url(r'^boss_chm_tracker/', views.boss_chm_tracker, name = 'boss_chm_tracker'),	
	url(r'^generate_invoice_boss_select/', views.generate_invoice_boss_select, name = 'generate_invoice_boss_select'),
	url(r'^submit_invoice_boss_selected/', views.submit_invoice_boss_selected, name = 'submit_invoice_boss_selected'),
	
	url(r'^check_uncheck_invoice/', views.check_uncheck_invoice, name = 'check_uncheck_invoice'),
	url(r'^submit_boss_client_details/', views.submit_boss_client_details, name = 'submit_boss_client_details'),
	url(r'^update_client_chm_details/', views.update_client_chm_details, name = 'update_client_chm_details'),
	url(r'^client_handler/', views.client_handler, name = 'client_handler'),
	url(r'^client_handler_boss/', views.client_handler_boss, name = 'client_handler_boss'),
	################# Login
	url(r'^user_login', views_login.user_login, name = 'user_login'),
	url(r'^user_logout', views_login.user_logout, name = 'user_logout'),
	url(r'^user_entry', views_login.user_entry, name = 'user_entry'),
	# url(r'^usertype_selecthandler', views_login.usertype_selecthandler, name = 'usertype_selecthandler'),

	################# Address Entry
	url(r'^address_entry/', views.address_entry, name = 'address_entry'),	
	url(r'^submit_ship_address_for_address/', views.submit_ship_address_for_address, name = 'submit_ship_address_for_address'),	
	url(r'^edit_invoice_details/', views.edit_invoice_details, name = 'edit_invoice_details'),	
	url(r'^get_invoice_template/', views.get_invoice_template, name = 'get_invoice_template'),	

	url(r'^generator', views.generator, name = 'generator'),
	url(r'^get_proj_name_list', views.get_proj_name_list, name = 'get_proj_name_list'),
	url(r'^get_pool_list', views.get_pool_list, name = 'get_pool_list'),
	url(r'^get_data', views.get_data, name = 'get_data'),
	url(r'^update_invoice_template', views.update_invoice_template, name = 'update_invoice_template'),
	url(r'^delete_invoice_template', views.delete_invoice_template, name = 'delete_invoice_template'),

	url(r'^chm_select_ship_address', views.chm_select_ship_address, name = 'chm_select_ship_address'),
	url(r'^chm_update_ship_address', views.chm_update_ship_address, name = 'chm_update_ship_address'),
	url(r'^chm_address_entry', views.chm_address_entry, name = 'chm_address_entry'),
	url(r'^chm_pool_entry', views.chm_pool_entry, name = 'chm_pool_entry'),
	url(r'^submit_pool_address', views.submit_pool_address, name = 'submit_pool_address'),
	url(r'^chm_select_pool_address', views.chm_select_pool_address, name = 'chm_select_pool_address'),
	url(r'^chm_update_pool_address', views.chm_update_pool_address, name = 'chm_update_pool_address'),

	url(r'^boss_address_entry', views.boss_address_entry, name = 'boss_address_entry'),
	url(r'^boss_select_pool_address', views.boss_select_pool_address, name = 'boss_select_pool_address'),
	url(r'^boss_select_ship_address', views.boss_select_ship_address, name = 'boss_select_ship_address'),
	url(r'^boss_update_ship_address', views.boss_update_ship_address, name = 'boss_update_ship_address'),
	url(r'^submit_boss_ship_for_address', views.submit_boss_ship_for_address, name = 'submit_boss_ship_for_address'),
	
	url(r'^welcome_chp_api', api_details.welcome_chp_api, name = 'welcome_chp_api'),
	#url(r'^update_client_details', api_details.update_client_details, name = 'update_client_details'),

	########### mail tracker
	url(r'^mail_tracker', views.mail_tracker, name = 'mail_tracker'),
	url(r'^select_client_handler', views.select_client_handler, name = 'select_client_handler'),
	url(r'^select_invoice_no_mail', views.select_invoice_no_mail, name = 'select_invoice_no_mail'),
	url(r'^attached_mail_details', views.attached_mail_details, name = 'attached_mail_details'),

	url(r'^mail_send', views.mail_send, name = 'mail_send'),

	############# Pool Master #####################################
	url(r'^pool_master/', views.pool_master, name = 'pool_master'),
	url(r'^submit_pool_master/', views.submit_pool_master, name = 'submit_pool_master'),
	url(r'^update_pool_master/', views.update_pool_master, name = 'update_pool_master'),
	
	url(r'^show_folder/', views.show_folder, name = 'show_folder'),
	url(r'^show_fold/', views.show_fold, name = 'show_fold'),

	url(r'^vaild_boss_invoice_details/', views.vaild_boss_invoice_details, name = 'vaild_boss_invoice_details'),
	url(r'^filter_invoice_tracker/', views.filter_invoice_tracker, name = 'filter_invoice_tracker'),
	url(r'^update_rate_exchange/', views.update_rate_exchange, name = 'update_rate_exchange'),

	url(r'^total_generated_chm_boss/', views.total_generated_chm_boss, name = 'total_generated_chm_boss'),
	url(r'^total_paid_invoice/', views.total_paid_invoice, name = 'total_paid_invoice'),
	url(r'^total_pending_invoice/', views.total_pending_invoice, name = 'total_pending_invoice'),
	url(r'^total_cancelled_invoice/', views.total_cancelled_invoice, name = 'total_cancelled_invoice'),
	url(r'^mail_log/', views.mail_log, name = 'mail_log'),
	url(r'^total_generated_usd_only/', views.total_generated_usd_only, name = 'total_generated_usd_only'),
	url(r'^total_paid_invoice_usd_only/', views.total_paid_invoice_usd_only, name = 'total_paid_invoice_usd_only'),
	url(r'^total_pending_invoice_usd_only/', views.total_pending_invoice_usd_only, name = 'total_pending_invoice_usd_only'),
	url(r'^total_cancelled_invoice_usd_only/', views.total_cancelled_invoice_usd_only, name = 'total_cancelled_invoice_usd_only'),
	url(r'^select_project_handler/', views.select_project_handler, name = 'select_project_handler'),
	url(r'^select_client_for_pool/', views.select_client_for_pool, name = 'select_client_for_pool'),
	#url(r'^select_price_type/', views.select_price_type, name = 'select_price_type'),
	url(r'^update_password/', change_password.update_password, name = 'update_password'),
	url(r'^change_update_details/', change_password.change_update_details, name = 'change_update_details'),
	url(r'^selected_currency_type_handler', views.selected_currency_type_handler, name = 'selected_currency_type_handler'),

	url(r'^export_tracker', export_tracker.export_tracker, name = 'export_tracker'),
	url(r'^invoice_export', export_tracker.invoice_export, name = 'invoice_export'),

	url(r'^selected_pending_invoice_no', pending_invoice.selected_pending_invoice_no, name = 'selected_pending_invoice_no'),
	url(r'^generate_of_pending_invoice', pending_invoice.generate_of_pending_invoice, name = 'generate_of_pending_invoice'),
	url(r'^get_invoice_calc', pending_invoice.get_invoice_calc, name = 'get_invoice_calc'),	

	url(r'^del_invoice_log', delx.del_invoice_log, name = 'del_invoice_log'),
	url(r'^total_deleted_chm_usd', delx.total_deleted_chm_usd, name = 'total_deleted_chm_usd'),
	url(r'^total_deleted_inr', delx.total_deleted_inr, name = 'total_deleted_inr'), 
	url(r'^entry_for_price_type', delx.entry_for_price_type, name = 'entry_for_price_type'), 


	url(r'^folder_list', delx.folder_list, name = 'folder_list'), 
	url(r'^folder_listx_for_boss', delx.folder_listx_for_boss, name = 'folder_listx_for_boss'), 

	url(r'^vaild_poompuhar_invoice_details', views.vaild_poompuhar_invoice_details, name = 'vaild_poompuhar_invoice_details'),
	url(r'^vaild_apeejay_invoice_details', views.vaild_apeejay_invoice_details, name = 'vaild_apeejay_invoice_details'),
	url(r'^template_download/', apj.template_download, name = 'template_download'),
	url(r'^other_template_download/', ck.other_template_download, name = 'other_template_download'),
	url(r'^shell_template_download/', sh.shell_template_download, name = 'shell_template_download'),
	url(r'^mail_format/', mf.mail_format, name = 'mail_format'),
	url(r'^vaild_clearlake_invoice_details/', views.vaild_clearlake_invoice_details, name = 'vaild_clearlake_invoice_details'),

	url(r'^boss_tracker/', btr.boss_tracker, name = 'boss_tracker'),	
	url(r'^filter_boss_invoice_tracker/', btr.filter_boss_invoice_tracker, name = 'filter_boss_invoice_tracker'),
	url(r'^chm_tracker/', ctr.chm_tracker, name = 'chm_tracker'),	
	url(r'^filter_chm_invoice_tracker/', ctr.filter_chm_invoice_tracker, name = 'filter_chm_invoice_tracker'),	

	url(r'^inr_tracker/', inr.inr_tracker, name = 'inr_tracker'),	
	url(r'^filter_inr_tracker/', inr.filter_inr_tracker, name = 'filter_inr_tracker'),	

	url(r'^cost_per_route/', cpr.cost_per_route, name = 'cost_per_route'),
	url(r'^update_cost_route/', cpr.update_cost_route, name = 'update_cost_route'),	
	url(r'^submit_cost_route/', cpr.submit_cost_route, name = 'submit_cost_route'),	
	url(r'^delete_cost_route/', cpr.delete_cost_route, name = 'delete_cost_route'),
	url(r'^invoice_no/', i.invoice_no, name = 'invoice_no'),
	url(r'^update_invoice_tag/', i.update_invoice_tag, name = 'update_invoice_tag'),
	url(r'^summary_report/', sr.summary_report, name = 'summary_report'),
	url(r'^summary_details_export/', sr.summary_details_export, name = 'summary_details_export'),
	# url(r'^other_invoice/', ot.other_invoice, name = 'other_invoice'),
	# url(r'^get_other_invoice/', ot.get_other_invoice, name = 'get_other_invoice'),
	# url(r'^submit_other_invoice/', ot.submit_other_invoice, name = 'submit_other_invoice'),
	url(r'^boss_export_tracker/', eb.boss_export_tracker, name = 'boss_export_tracker'),
	url(r'^inr_export_tracker/', ei.inr_export_tracker, name = 'inr_export_tracker'),
	url(r'^invoice_entry/', ie.invoice_entry, name = 'invoice_entry'),
	url(r'^get_other_invoice/', ie.get_other_invoice, name = 'get_other_invoice'),
	url(r'^submit_other_invoice/', ie.submit_other_invoice, name = 'submit_other_invoice'),
	url(r'^get_pool_details/', ie.get_pool_details, name = 'get_pool_details'),
	url(r'^get_address_details/', ie.get_address_details, name = 'get_address_details'),

	url(r'^filter_for_json_data/', jsx.filter_for_json_data, name = 'filter_for_json_data'),
	url(r'^get_json_data/', jsx.get_json_data, name = 'get_json_data'),	
	url(r'^connection_smb/', conn.connection_smb, name = 'connection_smb'),	
	url(r'^upload_excel/', ue.upload_excel, name = 'upload_excel'),
	url(r'^list/', ue.list, name = 'list'),
	url(r'^submit_upload_invoice/', ue.submit_upload_invoice, name = 'submit_upload_invoice'),
	url(r'^invoice_raise_summary/', rs.invoice_raise_summary, name = 'invoice_raise_summary'),
	# url(r'^invoice_raise_export/', rs.invoice_raise_export, name = 'invoice_raise_export'),
	# url(r'^tracker_summary/', rs.tracker_summary, name = 'tracker_summary'),
	url(r'^get_api_from_boss', fpi.get_api_from_boss, name = 'get_api_from_boss'),
	url(r'^get_vessel_list', fpi.get_vessel_list, name = 'get_vessel_list'),
	url(r'^get_account_list', fpi.get_account_list, name = 'get_account_list'),
	url(r'^export_from_api', fpi.export_from_api, name = 'export_from_api'),
	url(r'^api_invoice_export', fpi.api_invoice_export, name = 'api_invoice_export'),
	url(r'^export_summary_report', esr.export_summary_report, name = 'export_summary_report'),
	url(r'^export_summary_invoice', esr.export_summary_invoice, name = 'export_summary_invoice'),
	url(r'^export_dsr_details', dsrx.export_dsr_details, name = 'export_dsr_details'),
	url(r'^upload_files', uf.upload_files, name = 'upload_files'),
	url(r'^submit_upload_images', uf.submit_upload_images, name = 'submit_upload_images'),
	url(r'^view_payment', vpx.view_payment, name = 'view_payment'),
	url(r'^master_inv/', miv.master_inv, name = 'master_inv'),
	url(r'^get_client_details/', miv.get_client_details, name = 'get_client_details'),
	url(r'^submit_remittance_master/', miv.submit_remittance_master, name = 'submit_remittance_master'),
	url(r'^get_remittance_master/', miv.get_remittance_master, name = 'get_remittance_master'),
	url(r'^view_remittance/', miv.view_remittance, name = 'view_remittance'),
	url(r'^get_remittance_id/', miv.get_remittance_id, name = 'get_remittance_id'),
	
	url(r'^bank_statement/', bst.bank_statement, name = 'bank_statement'),
	url(r'^bank_entry_inr/', bst.bank_entry_inr, name = 'bank_entry_inr'),
	url(r'^bank_details_inr/', bst.bank_details_inr, name = 'bank_details_inr'),
	url(r'^del_details/', miv.del_details, name = 'del_details'),
	url(r'^delete_bank_statement_inr/', bst.delete_bank_statement_inr, name = 'delete_bank_statement_inr'),
	url(r'^update_bank_statement_inr/', bst.update_bank_statement_inr, name = 'update_bank_statement_inr'),
	#url(r'^get_bank_id_master/', bst.get_bank_id_master, name = 'get_bank_id_master'),

	url(r'^get_client_proj_details/', miv.get_client_proj_details, name = 'get_client_proj_details'),
	url(r'^update_remittance_master/', miv.update_remittance_master, name = 'update_remittance_master'),
	url(r'^bank_name/', bnx.bank_name, name = 'bank_name'),
	url(r'^other_bank_statement/', obs.other_bank_statement, name = 'other_bank_statement'),
	url(r'^other_bank_entry/', obs.other_bank_entry, name = 'other_bank_entry'),
	url(r'^other_bank_details/', obs.other_bank_details, name = 'other_bank_details'),
	#url(r'^other_get_bank_id_master/', obs.other_get_bank_id_master, name = 'other_get_bank_id_master'),
	url(r'^delete_invoice_for/', ctr.delete_invoice_for, name = 'delete_invoice_for'),
	url(r'^delete_invoice_for_usd/', btr.delete_invoice_for_usd, name = 'delete_invoice_for_usd'),
	url(r'^delete_invoice_for_inr/', inr.delete_invoice_for_inr, name = 'delete_invoice_for_inr'),
	url(r'^delete_bank_details/', obs.delete_bank_details, name = 'delete_bank_details'),
	#url(r'^delete_bank_del_sbi/', bst.delete_bank_del_sbi, name = 'delete_bank_del_sbi'),

	url(r'^payment_advice/', pa.payment_advice, name = 'payment_advice'),
	url(r'^submit_advice/', pa.submit_advice, name = 'submit_advice'),
	url(r'^delete_advice/', pa.delete_advice, name = 'delete_advice'),
	url(r'^edit_advice/', pa.edit_advice, name = 'edit_advice'),
	url(r'^get_currency_type/', pa.get_currency_type, name = 'get_currency_type'),
	
	url(r'^pid_advice/', pid.pid_advice, name = 'pid_advice'),
	url(r'^pid_submit_advice/', pid.pid_submit_advice, name = 'pid_submit_advice'),
	url(r'^pid_delete_advice/', pid.pid_delete_advice, name = 'pid_delete_advice'),
	url(r'^pid_edit_advice/', pid.pid_edit_advice, name = 'pid_edit_advice'),
	url(r'^pid_get_currncy_type/', pid.pid_get_currncy_type, name = 'pid_get_currncy_type'),

	url(r'^get_uploading_file_name/', pa.get_uploading_file_name, name = 'get_uploading_file_name'),
	url(r'^get_upload_file_name/', pid.get_upload_file_name, name = 'get_upload_file_name'),
	
	url(r'^single_data/', ds.single_data, name = 'single_data'),
	url(r'^single/', ds.single, name = 'single'),
	url(r'^update_single_invoice/', ds.update_single_invoice, name = 'update_single_invoice'),

	url(r'^get_fetch_api/', gfa.get_fetch_api, name = 'get_fetch_api'),
	url(r'^client_fetch_data/', gfa.client_fetch_data, name = 'client_fetch_data'),

	url(r'^get_client_api/', gca.get_client_api, name = 'get_client_api'),

	url(r'^export_invoice_template/', eis.export_invoice_template, name = 'export_invoice_template'),
	url(r'^other_export_download/', eis.other_export_download, name = 'other_export_download'),

	#url(r'^reconciliation/', rec.reconciliation, name = 'reconciliation'),
	#url(r'^reconciliation_entry/', rec.reconciliation_entry, name = 'reconciliation_entry'),
	url(r'^reconciliation_details/', rec.reconciliation_details, name = 'reconciliation_details'),
	url(r'^get_amount_value10/', rec.get_amount_value10, name = 'get_amount_value10'),

	url(r'^edit_remittance_list/', rec.edit_remittance_list, name = 'edit_remittance_list'),


	url(r'^client_data/', cj.client_data, name = 'client_data'),
	url(r'^client_list/', cj.client_list, name = 'client_list'),
	url(r'^client_log/', cj.client_log, name = 'client_log'),
	url(r'^get_currency_list/', cj.get_currency_list, name = 'get_currency_list'),
	url(r'^currency_entry/', cj.currency_entry, name = 'currency_entry'),
	url(r'^voyage_data/', jsx.voyage_data, name = 'voyage_data'),
	
	url(r'^export_dsr_download/', dsrx.export_dsr_download, name = 'export_dsr_download'),
	url(r'^export_fetch_api_data/', gfa.export_fetch_api_data, name = 'export_fetch_api_data'),
	url(r'^export_api_data/', gfa.export_api_data, name = 'export_api_data'),

	url(r'^get_account_tab/', gat.get_account_tab, name = 'get_account_tab'),
	url(r'^account_fetch_details/', gat.account_fetch_details, name = 'account_fetch_details'),	

	url(r'^update_address_template/', uad.update_address_template, name = 'update_address_template'),

	url(r'^get_client_currency_handler/', pid.get_client_currency_handler, name = 'get_client_currency_handler'),

	url(r'^get_remittance/', rec.get_remittance, name = 'get_remittance'),
	url(r'^delete_remiitance/', rec.delete_remiitance, name = 'delete_remiitance'),

	url(r'^update_bank_statement/', obs.update_bank_statement, name = 'update_bank_statement'),
	url(r'^delete_bank_statement/', obs.delete_bank_statement, name = 'delete_bank_statement'),

	
	url(r'^invoice_paid_track/', ctr.invoice_paid_track, name = 'invoice_paid_track'),	
	url(r'^invoice_paid_track_usd/', btr.invoice_paid_track_usd, name = 'invoice_paid_track_usd'),	
	url(r'^filter_remiitance_data/', rec.filter_remiitance_data, name = 'filter_remiitance_data'),
	
	url(r'^export_remiitance_data/', rec.export_remiitance_data, name = 'export_remiitance_data'),


	url(r'^monthly_summary/', ms.monthly_summary, name = 'monthly_summary'),
	url(r'^load_data/', ms.load_data, name = 'load_data'),
	url(r'^export_load_data/', ms.export_load_data, name = 'export_load_data'),
	url(r'^download_load_data/', ms.download_load_data, name = 'download_load_data'),

	url(r'^other_invoice_type/', oit.other_invoice_type, name = 'other_invoice_type'),
	url(r'^show_invoice_template/', oit.show_invoice_template, name = 'show_invoice_template'),
	url(r'^get_generate_pdf/', oit.get_generate_pdf, name = 'get_generate_pdf'),

	url(r'^save_client_fetch_data/', gfa.save_client_fetch_data, name = 'save_client_fetch_data'),

	url(r'^account_data/', acc.account_data, name = 'account_data'),
	
	url(r'^account_list/', acc.account_list, name = 'account_list'),
	url(r'^account_log/', acc.account_log, name = 'account_log'),
	url(r'^reconciliation_inr/', rnr.reconciliation_inr, name = 'reconciliation_inr'),
	url(r'^reconciliation_inr_entry/', rnr.reconciliation_inr_entry, name = 'reconciliation_inr_entry'),
	url(r'^save_remittance_inr/', rnr.save_remittance_inr, name = 'save_remittance_inr'),
	url(r'^filter_remiitance_data_inr/', rnr.filter_remiitance_data_inr, name = 'filter_remiitance_data_inr'),
	url(r'^update_remittance_inr/', rnr.update_remittance_inr, name = 'update_remittance_inr'),
	url(r'^delete_remiitance_inr/', rnr.delete_remiitance_inr, name = 'delete_remiitance_inr'),

	url(r'^update_rate_for_pdf/', oit.update_rate_for_pdf, name = 'update_rate_for_pdf'),

	url(r'^home/', hg.home, name = 'home'),

	url(r'^chm_invoice_type/', cit.chm_invoice_type, name = 'chm_invoice_type'),
	url(r'^get_other_invoice_ctm/', cit.get_other_invoice_ctm, name = 'get_other_invoice_ctm'),

	url(r'^chm_entry/', ce.chm_entry, name = 'chm_entry'),
	url(r'^submit_chm_invoice_alag/', ce.submit_chm_invoice_alag, name = 'submit_chm_invoice_alag'),

	url(r'^update_bank_entry/', bnx.update_bank_entry, name = 'update_bank_entry'),

	# url(r'^other_data/', od.other_data, name = 'other_data'),
)

urlpatterns+=(
	url(r'^get_pdf_viewer/', ctr.get_pdf_viewer, name = 'get_pdf_viewer'),	

)



