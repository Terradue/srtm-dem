#!/bin/env python
# mosaic geo-tiff SRTM V4 DEM
# create roi-pac or Gamma headers
# by Ran Novitsky Nof 2011


import Image,sys,os,glob,getopt,scipy.misc,time
from pylab import *
from string import join

def usage():
  sys.exit("""
Getting SRTM v4 DEM and preparing it for ROI_PAC or Gamma processing

usage:

    """+ sys.argv[0] +""" lat lon output [-g]  [-M site] [-s] [-h]

    lat,lon       : latitude and longitude in decimal degrees    
    output        : DEM output file name  
                    no file extention needed.
    -g            : Produce Gamma DEM only (4 byte real - big endien format)
                    default is to produce ROI-PAC DEM only (2 byte integer
                    - machine endien format)
   -D DEMDIR      : Path to SRTM dem zip files,
                    if ommited will be downloaded 
                    via default site:'jrc'
   -M site        : Mirror site to download files from. 
                    can be 'http' or 'ftp' where:
     ftp: ftp://xftp.jrc.it/pub/srtmV4/arcasci/ (default)
     http: http://srtm.geog.kcl.ac.uk/portal/srtm41/srtm_data_arcascii/ 
    -s            : Save a hillshade image of the DEM.
    -h            : Print this help text.
    
    The code will create a mosaicked DEM for use by ROI-PAC
    and Gamma interferometry software.
    
    SRTM data is available from:
    http://srtm.csi.cgiar.org/
    
    The script assumes that the files are adjuctant tiles. 
    Missing tiles will get zero values.
        
    Created by Ran Novitsky Nof, 2012
    last update: Jan 11, 2012
""")

ers2dtypes ={
"IEEE4ByteReal" : float32,
"IEEE8ByteReal" : float64,
"Signed32BitInteger" : int32,
"Signed16BitInteger" : int16,
"Signed8BitInteger" : int8,
"Unsigned32BitInteger" : uint32,
"Unsigned16BitInteger" : uint16,
"Unsigned8BitInteger" : uint8,
"Complex64"           : complex64
}

ByteOrders = {"LSBFirst" : "little","MSBFirst" : "big"}

locations = {
'ftp' : 'ftp://xftp.jrc.it/pub/srtmV4/tiff/',
'http': 'http://srtm.geog.kcl.ac.uk/portal/srtm41/srtm_data_geotiff/'
}

class SRTM:
    """class for SRTM DEM
    name = '' 				# Name of file 
    path = ''				# The path to the file
    byteorder = "little" # byte order
    dim = 0.0e-00			# pixel dimetions	
    width = 0				# number of sampels in each row
    length = 0				# number of rows
    east = 0.				# longitude coordinates of upper left corner 
    north = 0.				# latitude coordinates of upper left corner 
    im = ''         # DEM TIFF image data
    data = array([])				# DEM data values holder 
    ."""
    __name__ = 'SRTM'
    def __array__(self):
      return self
    def __call__(self):
      return 'SRTM'
    def __init__(self,filename):
      self.path,self.name = os.path.split(filename)
      if self.path == '': self.path='.'  
      self.dim = 0.0e-00
      self.width = 0
      self.length = 0
      self.east = 0.
      self.north = 0.
      self.im = ''
      self.byteorder = sys.byteorder
      self.data = array([])
      self.getdata()
    def __str__(self):
      return 'name = '+repr(self.name)+'\npath = '+repr(self.path)+'\ndim = '+repr(self.dim)+'\nwidth = '+repr(self.width)+'\nlength = '+repr(self.length)+'\neast = '+repr(self.east)+'\nnorth = '+repr(self.north)+'\n'
    def getdata(self):
      if (os.path.exists(self.path+os.sep+self.name)):
        self.im = Image.open(self.path+os.sep+self.name)
        self.im.mode = "I"
        self.dim = self.im.tag.get(33550)[0]
        self.width = self.im.tag.get(256)[0]
        self.length = self.im.tag.get(257)[0]
        self.east = self.im.tag.get(33922)[3]
        self.north = self.im.tag.get(33922)[4]
        self.data = scipy.misc.fromimage(self.im).astype(float32)
        self.data[where(self.data==0)] = 0.00001
        self.data[where(self.data==-32768)] = 0
    def ers_header(self):
      header='''DatasetHeader Begin 
        Version = "6.4"
        Name ="'''+self.name+'''.dem.ers"
        LastUpdated     = '''+time.strftime("%a %b %d %H:%M:%S GMT %Y",time.gmtime())+''' 
        DataSetType     = ERStorage 
        DataType        = Raster 
        ByteOrder       = '''+[b for b in ByteOrders if ByteOrders[b]==self.byteorder][0]+'''
        CoordinateSpace Begin 
                Datum = "WGS84"
                Projection = "GEODETIC"
                CoordinateType  = EN 
                Rotation        = 0:0:0.0 
        CoordinateSpace End 
        RasterInfo Begin 
               CellType        = '''+[b[0] for b in ers2dtypes.items() if self.data.dtype.type in b][0]+''' 
               NullCellValue   = 0 
                CellInfo Begin 
                        Xdimension      = '''+str(self.dim)+''' 
                        Ydimension      = '''+str(self.dim)+'''
                CellInfo End 
                NrOfLines       = '''+str(int(self.length))+'''
                NrOfCellsPerLine        = '''+str(int(self.width))+''' 
                RegistrationCoord Begin 
                        Eastings        = '''+str(self.east-self.dim/2.)+''' 
                        Northings       = '''+str(self.north+self.dim/2.)+'''
                RegistrationCoord End 
               NrOfBands       =  1
               BandId Begin 
                        Value = "Elevation"
               BandId End
        RasterInfo End 
DatasetHeader End'''
      savetxt(self.path+os.sep+self.name+'.dem.ers',[header],'%s')        
    def roi_header(self):
      header='''WIDTH         '''+str(self.width)+'''
FILE_LENGTH   '''+str(self.length)+'''
XMIN          0
XMAX          '''+str(self.width-1)+'''
YMIN          0
YMAX          '''+str(self.length-1)+'''
X_FIRST       '''+str(self.east)+'''
Y_FIRST       '''+str(self.north)+'''
X_STEP        '''+str(self.dim)+'''
Y_STEP        '''+str(-self.dim)+'''
X_UNIT        degres
Y_UNIT        degres
Z_OFFSET      0
Z_SCALE       1
PROJECTION    LATLON
DATUM         WGS84
'''
      savetxt(self.path+os.sep+self.name+'.dem.rsc',[header],'%s')
    def gamma_header(self):
      header='''Gamma DIFF&GEO DEM/MAP parameter file
title: '''+self.name+'''
DEM_projection:     EQA
data_format:        REAL*4
DEM_hgt_offset:          0.00000
DEM_scale:               1.00000
width:                '''+str(self.width)+'''
nlines:               '''+str(self.length)+'''
corner_lat:     '''+str(self.north)+'''  decimal degrees
corner_lon:     '''+str(self.east)+'''  decimal degrees
post_lat:   -'''+str(self.dim)+'''  decimal degrees
post_lon:    '''+str(self.dim)+'''  decimal degrees

ellipsoid_name: WGS 84
ellipsoid_ra:        6378137.000   m
ellipsoid_reciprocal_flattening:  298.2572236

datum_name: WGS 1984
datum_shift_dx:              0.000   m
datum_shift_dy:              0.000   m
datum_shift_dz:              0.000   m
datum_scale_m:         0.00000e+00
datum_rotation_alpha:  0.00000e+00   arc-sec
datum_rotation_beta:   0.00000e+00   arc-sec
datum_rotation_gamma:  0.00000e+00   arc-sec
datum_country_list Global Definition, WGS84, World
'''
      savetxt(self.path+os.sep+self.name+'.dem.par',[header],'%s') 
    def save_SRTM(self):
      self.data.tofile(self.path+os.sep+self.name+'.dem')
      self.ers_header()
    def imsave(self,outfile=0):
      slope = zeros_like(self.data)
      slope = (self.data[:,2:]-self.data[:,:-2])/(2*self.dim)
      mn,mx = slope[:,2:-2].min(),slope[:,2:-2].max()
      slope[:,2:-2] = (slope[:,2:-2]-mn)/float(mx-mn)*255
      slope[where(self.data==0)] = 0
      self.im = Image.fromarray(slope.astype(uint8))
      if not outfile: outfile = self.name+'.dem.jpg'
      self.im.save(outfile)
      self.im.show()
 
 
def get_needed_zipfiles(lat,lon):
  # getting four corners (delta = 1 deg from lat/lon)
  north = lat + 1
  south = lat - 1
  east  = lon - 1
  west  = lon + 1
  #getting needed tile indeces
  te = str(int(east+180)/5+1).zfill(2)
  tw = str(int(west+180)/5+1).zfill(2)
  tn = str(int(60-north)/5+1).zfill(2)
  ts = str(int(60-south)/5+1).zfill(2)
  # setting file names needed
  files = list(set(["srtm_"+te+"_"+tn+".tif","srtm_"+tw+"_"+tn+".tif","srtm_"+te+"_"+ts+".tif","srtm_"+tw+"_"+ts+".tif"]))
  print '\tlooking for files: '+join(files,', ')
  return files

def wget_zip_files(files,M='ftp',D='./'):
  for zipfile in files:
    if not os.path.exists(zipfile):
      if not D.endswith(os.sep): D=D+os.sep
      if os.path.exists(D+zipfile):
        print "\tlinking to zip file from "+D
        os.system("ln -s "+D+zipfile+' '+zipfile)
      elif M in locations:
        print "\tdownloading from cgiar sites..."
        os.system("wget --no-proxy "+locations[M]+zipfile)
      else:
        if not M.endswith(os.sep): M=M+os.sep
        print "\tdownloading from provided mirror site..."
        os.system("wget --no-proxy "+M+zipfile)
    else:
      print "\t"+zipfile+" is already in curent directory, skipping"
    if not os.path.exists(zipfile): 
      sys.exit("could not find "+zipfile)

def unzipfiles(files):
  print '\tunzippng files...'
  tiffiles = []
  for zipfile in files:
    if not os.path.exists(os.path.splitext(zipfile)[0]+'.tif'):
    	os.system("unzip -nL "+zipfile)
    tiffiles = tiffiles+[os.path.splitext(zipfile)[0]+'.tif']       
  return tiffiles
  
def get_dem_files(dem_files):
  print "\tReading SRTM files..."
  dem_files.sort()
  dems = []
  for dem in dem_files:
    dems = dems +[SRTM(D+dem)]
    print(D+dem)
  return dems
  
def get_dems_extent(dems):
  return min([dem.east for dem in dems]),max([dem.east+dem.width*dem.dim for dem in dems]),min([dem.north-dem.length*dem.dim for dem in dems]),max([dem.north for dem in dems]),dems[0].dim

def stich(srtm,dem):
  srtm.data[int(round((srtm.north-dem.north)/dem.dim)):int(round((srtm.north-dem.north)/dem.dim+dem.length)),int(round((dem.east-srtm.east)/dem.dim)):int(round((dem.east-srtm.east)/dem.dim+dem.width))] = dem.data[:,:]

def mk_srtm(outfile,lat,lon,M='ftp',D='./'):
  files = get_needed_zipfiles(lat,lon)
  #wget_zip_files(files,M,D)
  #files = unzipfiles(files)
  dems = get_dem_files(files)
  srtm = SRTM(outfile)  
  west,east,south,north,dim = get_dems_extent(dems)
  srtm.dim = dim
  srtm.width = int(round((east-west)/dim))
  srtm.length = int(round((north-south)/dim))
  srtm.east = west
  srtm.north = north
  srtm.data = zeros((srtm.length,srtm.width),dtype=float32)
  print "\tMosaic SRTM files..."
  for dem in dems:
    stich(srtm,dem)
  srtm.im = scipy.misc.toimage(srtm.data)
  return srtm
  
  

if __name__=="__main__":
  print " ****** Mosaic SRTM DEM ******"
  try:
    opts,args = getopt.gnu_getopt(sys.argv[3:],'ghsM:D:')
  except getopt.error, err:
    print str(err)
    usage()
  opts = dict(opts)
  args
  if '-h' in opts: usage()
  try:
    outfile = args[0]
  except IndexError:
    print "Error: no output name"
    usage()
  try:
    lat = float(sys.argv[1])
  except IndexError:
    print "Error: no latitude value"
    usage()
  try:
    lon = float(sys.argv[2])
  except IndexError:
    print "Error: no longitude value"
    usage() 
  if lat>90 or lat<-90:
    print "Latitude should be in range -90:90"
    usage()
  if lon>180 or lon<-180:
    print "Longitude should be in range -180:180"
    usage()       
  if '-M' in opts:
    M = opts['-M']
  else:
    M = 'ftp'
  if '-D' in opts:
    D = opts['-D']
  else:
    D = './'  
  srtm = mk_srtm(outfile,lat,lon,M,D) 
  if '-s' in opts:
    print "\tSaving to jpg image..."
    srtm.imsave()
    print "\tShowing "+srtm.name+".dem.jpg"
  if '-g' in opts:
    print "\tSaving "+srtm.name+".dem to Gamma format..."
    srtm.data = srtm.data.astype(float32)
    if sys.byteorder=='little':
      srtm.data = srtm.data.byteswap().astype(float32)
      srtm.byteorder = 'big'
    srtm.gamma_header()
  else:
    print "\tSaving "+srtm.name+".dem to ROI-PAC format..."
    srtm.data = srtm.data.astype(int16)
    srtm.roi_header()
  srtm.save_SRTM()  

  
  
