# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Producttemplate(models.Model):
   
    _inherit = "product.template"
    special_delivery_customer = fields.Boolean(string="Livraison Spéciale")
    variete = fields.Char('Variété')
    sexe = fields.Char('Sexe')
    taille = fields.Char('Taille')
    age = fields.Char('Age')
    bac = fields.Char('Bac')
    qualite = fields.Char('Qualité')
    eleveur = fields.Char('Eleveur')
    lien_video = fields.Char('Lien vidéo')
    
class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = "product.product"

    heart_icon = fields.Boolean(string="Coup de Coeur",  )
    special_delivery_b2c = fields.Boolean(string="Livraison Spéciale B2C",  )
    special_delivery_customer = fields.Boolean(string="Livraison Spéciale Client",  )

    critere_nourriture_6c_8c = fields.Boolean(string="Critère Nourriture 6°C-8°C",  )
    critere_nourriture_8c_15c = fields.Boolean(string="Critère Nourriture 8°C-15°C",  )
    critere_nourriture_moin_15c = fields.Boolean(string="Critère Nourriture 15°C<",  )
    critere_nourriture_plus_1_an = fields.Boolean(string="Critère Nourriture 0 à 1 an",  )
    critere_nourriture_un_deux_ans = fields.Boolean(string="Critère Nourriture 1 à 2 ans",  )
    critere_nourriture_plus_3_ans = fields.Boolean(string="Critère Nourriture 3 ans +",  )
    taille_s = fields.Boolean(string="Taille S 3 mm",  )
    taille_m = fields.Boolean(string="Taille M 5 mm",  )
    taille_l = fields.Boolean(string="Taille L 8 mm",  )
    display_vente = fields.Boolean(string="En vente sur site", default=True)

