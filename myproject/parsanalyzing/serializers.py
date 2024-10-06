from rest_framework import serializers
from parsanalyzing.models import Parsanalyze, BestForBuying


class ParsanalyzeSerializer(serializers.HyperlinkedModelSerializer):
    # highlight = serializers.HyperlinkedIdentityField(view_name=
    #     'parsanalyzing-highlight', format='html')
    class Meta:
        model = Parsanalyze
        fields = ['url', 'id', 'title', 'book_price', 'curr_price', 'sfrw_price', 'lfrw_price']

    def create(self, validated_data):
        """
        Create and return a new `Parsanalyze` instance, given the validated data.
        """
        return Parsanalyze.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Parsanalyze` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.book_price = validated_data.get('book_price', instance.book_price)
        instance.curr_price = validated_data.get('curr_price', instance.curr_price)
        instance.sfrw_price = validated_data.get('sfrw_price', instance.sfrw_price)
        instance.lfrw_price = validated_data.get('lfrw_price', instance.lfrw_price)
        instance.save()
        return instance


class BestForBuyingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BestForBuying
        fields = ['url', 'id', 'full_title', 'short_title']

    def create(self, validated_data):
        return BestForBuying.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.full_title = validated_data.get('full_title', instance.full_title)
        instance.short_title = validated_data.get('short_title', instance.short_title)
        instance.save()
        return instance
