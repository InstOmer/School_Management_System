from rest_framework import serializers
from meet.models import Meet
from django.contrib.auth import get_user_model


User = get_user_model()


class MeetSerializer(serializers.ModelSerializer):
    
    participants = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(), many=True
    )
    
    class Meta:
        
        model = Meet
        fields = ["id", "meet_name", "meet_date", "description", "location", "participants"]
        
    
    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        
        meet = Meet.objects.create(**validated_data)
        
        meet.participants.set(participants)
        
        return meet
    
    
    def update(self, instance, validated_data):
        participants = validated_data.pop("participants", None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        
        if participants is not None:
            instance.participants.set(participants)
            
        
        return instance