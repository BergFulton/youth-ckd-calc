from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe

class InputModel(models.Model):
	session_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	male_y1n0 = models.IntegerField(
		choices = (
	    	(1, "Male"),
	    	(0, "Female")),
    	default=None)
	age = models.IntegerField(choices=[(x, x) for x in range(2, 19)])
	ckddiag_g1ng0 = models.IntegerField(
		choices = (
			(0, "Non-glomerular diagnosis"),
			(1, "Glomerular diagnosis")),
		default=None)
	gfr_l1m2h3 = models.IntegerField(
		choices = (
			(1, mark_safe("< 30 ml/min|1.73m<sup>2</sup>")),
			(2, mark_safe("30 to 45 ml/min|1.73m<sup>2</sup>")),
			(3, mark_safe("&ge; 45 ml/min|1.73m<sup>2</sup>")),),
		default=None)
	yesnochoice = (
			(1, "Yes"),
			(0, "No"),
		)
	htn_y1n0 = models.IntegerField(choices=yesnochoice, default=None)
	hypoalb_y1n0 = models.IntegerField(choices=yesnochoice, default=None)
	hightrig_y1n0 = models.IntegerField(choices=yesnochoice, default=None,blank=False)
	lowhdl_y1n0 = models.IntegerField(choices=yesnochoice, default=None,blank=False)
	highnonhdl_y1n0 = models.IntegerField(choices=yesnochoice, default=None,blank=False)
	proteinuria_cur_y1n0 = models.IntegerField(choices=yesnochoice, default=None)
	anemia_cur_y1n0 = models.IntegerField(choices=yesnochoice, default=None)
	aceiarb_cur_y1n0 = models.IntegerField(choices=yesnochoice, default=None)
	proteinuria_past_y1n0 = models.IntegerField(choices=yesnochoice, default=None)
	anemia_past_y1n0 = models.IntegerField(choices=yesnochoice, default=None)
	aceiarb_past_y1n0 = models.IntegerField(choices=yesnochoice, default=None)