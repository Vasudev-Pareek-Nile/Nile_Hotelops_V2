from django.db import models
from datetime import date 
from django.contrib.auth.models import User
from PIL import Image
from moviepy.editor import VideoFileClip
import os



class Categories(models.Model):
    category_name = models.CharField(max_length=255)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

class Media_Asset_Library(models.Model):
    
    choice_type = (("Image","Image"),("Video","Video"))
    
    Title = models.CharField(max_length=100,null=False,blank=False)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,null=False,blank=False)
    Media = models.FileField(upload_to="media_asset_library", max_length=100)
    Thumbnail = models.ImageField(upload_to="media_asset_library/thumbnails", max_length=255, blank=True, null=True)

    
    Media_Type = models.CharField(choices=choice_type,max_length=20,default="Image") 
    Descriptions= models.TextField(null=False,blank=False)
    Upload_Date  = models.DateField(default=date.today)
    Expiration_Date = models.DateField()
    Upload_By= models.CharField(max_length=200,null=False,blank=False)
    For_Hotels  = models.CharField(max_length=200,null=False,blank=False)
    version = models.CharField(max_length=200,null=False,blank=False) 
    Original_Width = models.PositiveIntegerField(default=0)
    Original_Height = models.PositiveIntegerField(default=0)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Title + '==>' + self.Media_Type

    def save(self, *args, **kwargs):
            try:
                if self.Media_Type == 'Image':
                  with Image.open(self.Media.path) as img:
                    thumbnail_size = (200, 200)  
                    img.thumbnail(thumbnail_size)
                    thumbnail_path = self.Media.path.replace(".", "_thumbnail.")
                    img.save(thumbnail_path)
                    
                    self.Thumbnail = thumbnail_path
                        
                elif self.Media_Type == 'Video':
                    thumbnail_path = self.Media.path.replace(".mp4", "_thumbnail.jpg")  
                    self.generate_video_thumbnail(thumbnail_path)
                    self.Thumbnail.name = "media_asset_library/thumbnails/" + os.path.basename(thumbnail_path)
            except Exception as e:
                print(f"Error generating thumbnail: {e}")

            super().save(*args, **kwargs)

    def generate_video_thumbnail(self, thumbnail_path):
       
        try:
            video_path = self.Media.path
            video_clip = VideoFileClip(video_path)

            frame = video_clip.get_frame(0)
            print(f"Frame shape: {frame.shape}")

            thumbnail_img = Image.fromarray((frame * 1).astype('uint8'))

            thumbnail_size = (1080, 720)
            thumbnail_img.thumbnail(thumbnail_size)

            video_directory = os.path.dirname(video_path)
            thumbnail_filename = os.path.splitext(os.path.basename(video_path))[0] + "_thumbnail.jpg"
            thumbnail_path = os.path.join(video_directory, "thumbnails", thumbnail_filename)

            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
            thumbnail_img.save(thumbnail_path)

            print(f"Thumbnail saved at: {thumbnail_path}")
        except Exception as e:
            print(f"Error generating video thumbnail: {e}")    












        

