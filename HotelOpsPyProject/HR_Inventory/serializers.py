from rest_framework import serializers
from .models import HR_Inventory_Information, HR_Inventory_Details, HR_Inventory_Item_Master

class InventoryDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="HR_Inventory_Item_Master.ItemName", read_only=True)
    item_id = serializers.IntegerField(source="HR_Inventory_Item_Master.id")

    class Meta:
        model = HR_Inventory_Details
        fields = ["item_id", "item_name", "Item_Issued"]




class HRInventorySerializer(serializers.ModelSerializer):
    details = InventoryDetailSerializer(many=True)

    class Meta:
        model = HR_Inventory_Information
        fields = [
            "id", "EmpID", "EmployeeCode", "EmployeeName",
            "Department", "DesignationGrade", "ReportingtoDesigantion",
            "IssuedDate", "details"
        ]

    def create(self, validated_data):
        details_data = validated_data.pop("details")

        UN = HR_Inventory_Information.objects.create(**validated_data)

        for d in details_data:
            HR_Inventory_Details.objects.create(
                HR_Inventory_Information=UN,
                HR_Inventory_Item_Master_id=d["HR_Inventory_Item_Master"]["id"],
                Item_Issued=d["Item_Issued"]
            )

        return UN

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details")

        HR_Inventory_Details.objects.filter(
            HR_Inventory_Information=instance
        ).update(IsDelete=True)

        for d in details_data:
            HR_Inventory_Details.objects.create(
                HR_Inventory_Information=instance,
                HR_Inventory_Item_Master_id=d["HR_Inventory_Item_Master"]["id"],
                Item_Issued=d["Item_Issued"]
            )

        return instance
