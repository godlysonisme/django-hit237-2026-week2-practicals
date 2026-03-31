from django.db import models
from django.core.exceptions import ValidationError
 
 
 
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField()
 
 
    def __str__(self):
        return self.title[:25]
 
 
    # ===== FAT MODEL: Business Logic Methods =====
    
    @classmethod
    def create_post(cls, title, content, published_date=None):
        """
        Factory method to create and validate a new post.
        Centralizes post creation logic in the model.
        """
        from django.utils import timezone
        if not title or not content:
            raise ValidationError("Title and content are required.")
        
        post = cls(
            title=title,
            content=content,
            published_date=published_date or timezone.now()
        )
        post.full_clean()  # Validates all model constraints
        post.save()
        return post
 
 
    def update_post(self, title=None, content=None):
        """
        Update post fields with validation.
        Business logic ensures data integrity.
        """
        if title:
            self.title = title
        if content:
            self.content = content
        
        self.full_clean()  # Validate before saving
        self.save()
 
 
    def delete_post(self):
        """
        Delete post. Can be extended with soft deletes or business rules.
        """
        self.delete()
 
 
    @classmethod
    def get_published_posts(cls):
        """
        Retrieve all published posts ordered by date.
        Centralizes query logic in the model.
        """
        return cls.objects.filter(
            published_date__isnull=False
        ).order_by('-published_date')
 
 
    @classmethod
    def get_post_by_id(cls, pk):
        """
        Get post by ID or raise Http404.
        Centralizes this retrieval logic in the model.
        """
        from django.shortcuts import get_object_or_404
        return get_object_or_404(cls, pk=pk)
