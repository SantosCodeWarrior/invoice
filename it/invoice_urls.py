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
from it import manual_entry as mes
from it import client_json as cjs
from it import invoice_entry as ies
from it import bluewater as bwtw
from it import rpayment_advices as rpa
from it import h_reconciliation as h_rec
from it import online_dsr as odsr
from it import conv_rate as ctr
from it import master_tracker as mts
from it import rec_inr as rits
from it import view_rec_inr as vri
from it import ledger as lgx

urlpatterns = patterns('',
	url(r'^reconciliation/', rec.reconciliation, name = 'reconciliation'),
	#url(r'^reconciliation_entry/', rec.reconciliation_entry, name = 'reconciliation_entry'),
	url(r'^reconciliation_details/', rec.reconciliation_details, name = 'reconciliation_details'),
	url(r'^get_amount_value1/', rec.get_amount_value1, name = 'get_amount_value1'),	
	url(r'^get_amount_value2/', rec.get_amount_value2, name = 'get_amount_value2'),
	url(r'^get_amount_value3/', rec.get_amount_value3, name = 'get_amount_value3'),		
	url(r'^get_amount_value4/', rec.get_amount_value4, name = 'get_amount_value4'),	
	url(r'^get_amount_value5/', rec.get_amount_value5, name = 'get_amount_value5'),	
	url(r'^get_amount_value6/', rec.get_amount_value6, name = 'get_amount_value6'),	
	url(r'^get_amount_value7/', rec.get_amount_value7, name = 'get_amount_value7'),	

	url(r'^get_amount_value8/', rec.get_amount_value8, name = 'get_amount_value8'),	
	url(r'^get_amount_value9/', rec.get_amount_value9, name = 'get_amount_value9'),	
	url(r'^get_amount_value10/', rec.get_amount_value10, name = 'get_amount_value10'),

	url(r'^get_status/', rec.get_status, name = 'get_status'),
	

	url(r'^get_total_amount/', rec.get_total_amount, name = 'get_total_amount'),	
	url(r'^update_remittance_list/', rec.update_remittance_list, name = 'update_remittance_list'),	
	url(r'^calculation_remittance/', rec.calculation_remittance, name = 'calculation_remittance'),
	url(r'^reconciliation_entry/', rec.reconciliation_entry, name = 'reconciliation_entry'),
	url(r'^save_remittance/', rec.save_remittance, name = 'save_remittance'),
	url(r'^manual_entry/', mes.manual_entry, name = 'manual_entry'),
	url(r'^invoice_details_chm/', mes.invoice_details_chm, name = 'invoice_details_chm'),
	url(r'^update_invoice_details_chm/', mes.update_invoice_details_chm, name = 'update_invoice_details_chm'),
	url(r'^export_client_json/', cjs.export_client_json, name = 'export_client_json'),	
	url(r'^export_client_download/', cjs.export_client_download, name = 'export_client_download'),	
	url(r'^insert_for_new_client/', ies.insert_for_new_client, name = 'insert_for_new_client'),
	url(r'^export_reconciliation_download/', rec.export_reconciliation_download, name = 'export_reconciliation_download'),
	
	url(r'^fin_bluewater/', bwtw.fin_bluewater, name = 'fin_bluewater'),
	url(r'^update_fin_bluewater/', bwtw.update_fin_bluewater, name = 'update_fin_bluewater'),
	url(r'^gstin_details/', bwtw.gstin_details, name = 'gstin_details'),
	url(r'^gst_details_entry/', bwtw.gst_details_entry, name = 'gst_details_entry'),

	###Payment Advices Entry
	url(r'^rpayment_advices/', rpa.rpayment_advices, name = 'rpayment_advices'),
	url(r'^get_client_list/', rpa.get_client_list, name = 'get_client_list'),
	url(r'^insert_payment_advise/', rpa.insert_payment_advise, name = 'insert_payment_advise'),
	url(r'^h_reconciliation/', h_rec.h_reconciliation, name = 'h_reconciliation'),
	url(r'^inserting_remittance_data/', h_rec.inserting_remittance_data, name = 'inserting_remittance_data'),
	url(r'^calc_remittance_datas/', h_rec.calc_remittance_datas, name = 'calc_remittance_datas'),
	url(r'^submitting_remittance_data/', h_rec.submitting_remittance_data, name = 'submitting_remittance_data'),
	url(r'^load_dsr/', odsr.load_dsr, name = 'load_dsr'),
	url(r'^dsr_list/', odsr.dsr_list, name = 'dsr_list'),

	url(r'^conv_rate/', ctr.conv_rate, name = 'conv_rate'),
	url(r'^insert_for_conv_rate/', ctr.insert_for_conv_rate, name = 'insert_for_conv_rate'),
	url(r'^conv_rate_list/', ctr.conv_rate_list, name = 'conv_rate_list'),
	#url(r'^rate_price_list/', ctr.rate_price_list, name = 'rate_price_list'),
	url(r'^master_tracker/', mts.master_tracker, name = 'master_tracker'),
	url(r'^filter_master_tracker/', mts.filter_master_tracker, name = 'filter_master_tracker'),
	url(r'^export_master_trackerss/', mts.export_master_trackerss, name = 'export_master_trackerss'),
	url(r'^xexport_tracker_download/', mts.xexport_tracker_download, name = 'xexport_tracker_download'),
	url(r'^submit_approved_details/', rec.submit_approved_details, name = 'submit_approved_details'),
	url(r'^get_pdf_viewerx/', rec.get_pdf_viewerx, name = 'get_pdf_viewerx'),
	url(r'^rec_inr/', rits.rec_inr, name = 'rec_inr'),
	url(r'^calc_remittance_datas_inr/', rits.calc_remittance_datas_inr, name = 'calc_remittance_datas_inr'),
	url(r'^submitting_inr_data/', rits.submitting_inr_data, name = 'submitting_inr_data'),

	url(r'^filter_rec_inr/', vri.filter_rec_inr, name = 'filter_rec_inr'),
	url(r'^view_rec_inr/', vri.view_rec_inr, name = 'view_rec_inr'),
	url(r'^update_remiitance_inrs/', vri.update_remiitance_inrs, name = 'update_remiitance_inrs'),
	url(r'^calculation_remittance_inr/', vri.calculation_remittance_inr, name = 'calculation_remittance_inr'),
	url(r'^get_pdf_viewerx_inr/', vri.get_pdf_viewerx_inr, name = 'get_pdf_viewerx_inr'),

	url(r'^get_otp_plan', views_login.get_otp_plan, name = 'get_otp_plan'),
	url(r'^otp_verification', views_login.otp_verification, name = 'otp_verification'),

	url(r'^ledger/', lgx.ledger, name = 'ledger'),
	url(r'^ledger_datas/', lgx.ledger_datas, name = 'ledger_datas'),
	url(r'^export_ledger_data', lgx.export_ledger_data, name = 'export_ledger_data'),
	url(r'^export_legder_download', lgx.export_legder_download, name = 'export_legder_download'),
)



