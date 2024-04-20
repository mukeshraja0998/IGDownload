import instaloader
L = instaloader.Instaloader()
#old C3kKZk2PE34
#new https://www.instagram.com/p/C2YfSsSSbFk/?igsh=aGVocTI3Nnltb2Fw  -no

#https://www.instagram.com/reel/C2tvXlTI41f/?igsh=M3N2YTUyOXdzZm9q --yes 

#https://www.instagram.com/reel/C5qVV_1ROPD/?igsh=b3NtMWRwMGR4OXoy  -no
post = instaloader.Post.from_shortcode(L.context, "C2YfSsSSbFk")
video_url = post.video_url
filename = L.format_filename(post, target=post.owner_username)
L.download_pic(filename=filename, url=video_url, mtime=post.date_utc)




L = instaloader.Instaloader()
post_url = 'https://www.instagram.com/p/CgbAU5GD6MU/'
post = instaloader.Post.from_shortcode(L.context, post_url.split('p/')[1].strip('/ '))
photo_url = post.url   # this will be post's thumbnail (or first slide)
video_url = post.video_url  # if post.is_video is True then it will be url of video file
L.download_pic(filename=filename, url=photo_url, mtime=post.date_utc)

dp = instaloader.Instaloader()
profile_name=''
dp.download_profile(profile_name, profile_pic_only = True)


#https://www.instagram.com/p/C5S-SRyxNt3/?igsh=NjRkeDFsbW1tOWdn