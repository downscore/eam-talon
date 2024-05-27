# YouTube is currently the only media app where we support seeking or changing the playback speed.
# Consider moving these commands if this changes in the future.
media faster: user.youtube_increase_playback_speed()
media slower: user.youtube_decrease_playback_speed()
media push: user.youtube_seek_forward()
media pull: user.youtube_seek_backward()
