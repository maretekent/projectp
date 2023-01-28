# Models
class Section(models.Model):
	title = models.CharField(max_length=500)
	description = models.TextField(blank=True)
	user = models.ForeignKey(Profile, related_name="sections", on_delete=models.CASCADE)


class Feed(models.Model):
	title = models.CharField(max_length=500)
	link_rss = models.URLField(max_length=500)
	link_web = models.URLField(max_length=500)
	description = models.TextField(blank=True)
	language = models.CharField(max_length=50, blank=True)
	logo = models.URLField(blank=True)

	sections = models.ManyToManyField(Section, related_name="feeds")


# serializers

class FeedSerializer(serializers.ModelSerializer):
	sections = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = Feed
		fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
	feeds = FeedSerializer(many=True, read_only=True)

	class Meta:
		model = Section
		exclude = ('user',)
