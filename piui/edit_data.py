from models import Album, Artist


band = Artist.select().where(Artist.name == "Kutless").get()
print(band.name)

# shortcut method
band = Artist.get(Artist.name == "Kutless")
print(band.name)

# change band name
band.name = "Beach Boys"
band.save()

album = Album.select().join(Artist).where(
    (Album.title == "Thrive") & (Artist.name == "Newsboys")
    ).get()
album.title = "Step Up to the Microphone"
album.save()
