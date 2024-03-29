import pymongo
import pandas as pd
from pprint import pprint

if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000')
    data = client.python2122
    d = data.list_collection_names()
    album = data['albums']
    artist = data['artists']
    genre = data['genres']
    media = data['media_types']
    play = data['playlists']

    #cursor = album.find({})
    #cursor2 = artist.find({})

    #for d ,e in zip(cursor,cursor2):
    #    print(d.keys(),d['tracks'][0].keys())

    
    
    c = artist.find_one({})
    d = album.find_one({})
    e = genre.find_one({})
    f = media.find_one({})
    g = play.find_one({})
    #print(c.keys(), d.keys(), e.keys(), f.keys(), g.keys())
   # print(d, sep = '\n')
    
    l = data["albums"].aggregate([
    {"$lookup": {
         "from": "artists",
         "localField": "artist_id",
         "foreignField": "_id",
         "as": "artist"}}
    ,{'$project':{'ts':{'$and':[{'$gt':['tracks.millisecond',90000]},{'$lt':['$tracks.millisecond',120000]}] }}}])


   # l.find({'tracks.milliseconds' :{'$gt' :90000}})
  
   # print(l)
   # print(data['albums'].find_one({},{'tracks':{'name':1,'composer':1}}))
   # print(list(l),d['tracks'][0])
    l = data['albums'].aggregate([{'$lookup':{'from':'artists','localField':'artist_id','foreignField':'_id','as':'artist'}},{'$project':
        {'title':1,'tracks.name':1, 'tracks.composer':1,'tracks.milliseconds':1, 'artist.name':1 }}])
    aaa = list(l)
    result = []
    for i in range(len(aaa)):
        for j in range(len(aaa[i]['tracks'])):
                aaa[i]['tracks'][j]['album_name'] = aaa[i]['title']
                aaa[i]['tracks'][j]['artist_name'] = aaa[i]['artist'][0]['name']
    for i in range(len(aaa)):
            for j in range(len(aaa[i]['tracks'])):
                result.append(aaa[i]['tracks'][j])
    df = pd.DataFrame(result)
    #print(aaa[0])
    df_new = df[(df['milliseconds'] >= 90000) & (df['milliseconds'] <= 120000)]
    df_new = df_new.sort_values(by=['composer'], ascending = True, na_position = 'first')
    df_new.drop('milliseconds', axis=1, inplace=True)
    
   # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
   #     print(df_new)
    final = df_new.to_dict('records')
    bbb = list(final)
    for i in range(len(bbb)):
        bbb[i]['title'] = bbb[i].pop('name')

    new_order = ['title', 'composer', 'artist_name', 'album_name']
    for i in range(len(bbb)):
       bbb[i] =  {k: bbb[i][k] for k in new_order}


    print('length of list is :', len(bbb))
    for i in range(len(bbb)):
        print(bbb[i])
