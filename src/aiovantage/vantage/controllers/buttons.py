from aiovantage.aci_client.system_objects import Button
from aiovantage.hc_client import StatusType
from aiovantage.vantage.controllers.base import BaseController

# BTN <button vid>
#   -> R:BTN <button vid>
#      R:PRESS <button vid> "EVENT"
#      R:RELEASE <button vid> "EVENT"

# BTNPRESS <button vid>
#   -> R:PRESS <button vid> "EVENT"

# BTNRELEASE <button vid>
#   -> R:RELEASE <button vid> "EVENT"

# STATUS BTN
#   -> R:STATUS BTN
#   -> S:BTN <button vid> <"PRESS" | "RELEASE">

# ADDSTATUS <button vid>
#   -> R:ADDSTATUS <button vid>
#   -> S:STATUS <button vid> Button.GetState <0 | 1>
#   -> S:STATUS <button vid> LED.GetState <a b c d>
#   -> S:STATUS <button vid> Adjust.GetLevel <x>


class ButtonsController(BaseController[Button]):
    item_cls = Button
    vantage_types = ("Button",)
    status_types = (StatusType.BTN,)
