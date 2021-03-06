�
2o<Wc           @� s>  d  Z  d d l m Z m Z m Z d d l Z e j j d d � d d l Z d d l	 Z	 d d l
 Z
 d d l Z y, d d l m Z m Z m Z d d l Z Wn/ e k
 r� e e e f \ Z Z Z e Z n Xe j d d k r%d d l Z d d l Z d d l Z d d l m Z d d l Z nb e j d d	 k r�d d l Z d d
 l m Z d d l m Z d d l m Z d d l m Z n  d Z d Z  d a! d a" d a# d a$ d a% d a& d a' d Z( d Z) e	 j* d � Z+ e	 j* d � Z, e j j- d � Z. e j j- d � Z/ e j j- d � Z0 x: e. e/ e0 g D]) Z1 e j j2 e1 � rVe j3 e1 � n  q-We j j4 e0 d � Z5 e j j4 e0 d � Z6 d e Z7 d Z8 d  Z9 d! Z: d" Z; d# Z< d$ Z= d% Z> d# Z? d& Z@ d' ZA d( ZB d) ZC d* ZD d+ ZE d, ZF d- ZG d. ZH d/ ZI d0 ZJ d1 ZK d2 ZL d3 ZM d4 ZN d5 ZO d6 ZP d7 ZQ d8 ZR d9 ZS d: ZT d; ZU d< ZV d= ZW d< ZX d> ZY d< ZZ d? Z[ d@ Z\ dA Z] dB Z^ dC Z_ dD Z` dE Za dF Zb dG �  Zc dH �  Zd dI �  Ze dJ �  Zf dK eg f dL �  �  YZh dM �  Zi dN eg f dO �  �  YZj dP e jk f dQ �  �  YZl dR e jk f dS �  �  YZm dT �  Zn eo dU k r:en �  n  d S(V   u   Modify Fdi filesi����(   t   print_functiont   unicode_literalst   with_statementNi    u   library.zip(   t   Imaget	   ImageFontt	   ImageDrawu   2(   t   askcoloru   3(   t   ttk(   t
   filedialog(   t
   messageboxu   0.1.0u   Jini   i�  u   10u   100u   0u   %4d / %4d |%18s |%20su   TAXON_FREQUENCYu   TAXON_ORIG_FREQUENCYu   TAXON_FREQUENCY;\d+;u   TAXON_ORIG_FREQUENCY;\d+;u   ./outputu   ./imagesu   ./infou   data.txtu   info.txtu   Fdi Generator v%su   1000x750u   Browse Color...u   Choose Excel file: u   Browse xlsx file...u   ...u   Choose fdi file: u   Browse fdi file...u   Ignore Limit: u   Minimum Limit: u   Maximum Limit: u   Minimum Circle Radius: u   Maximum Circle Radius: u   Border Color: u   Info Line Style (info.txt): u   Output fdi filename: u
   output.fdiu   Executeu   Selected xlsx file: u   Selected fdi file: u   Excel erroru   No xlsx file was selectedu	   Fdi erroru   No Fdi file was selected!u   Execl erroru   No Execl file was selectedu   Color choose erroru   Not all colors were choosed!u   Output file erroru#   No valid output file was specified!u   Xlsx content erroru0   Blank or invalid xlsx cell (Row: %d, Column: %d)uP   First line of Xlsx file must be title (rather than digit) (Row: %d, Column: %d))ud   Xlsx Cells not in first line must be digit (rather than alpha or blank string) (Row: %d, Column: %d)u   Data inconsistent erroru5   Xlsx data inconsistent with Hap_* numbers in fdi fileu   Start validating data...u   Finished data validationu   Raw data processed!u   Info file generatedu   New fdf file generatedc         C� s�   t  g  |  j d d � j d d � j d � D] } t t | � � ^ q+ � } t r� t j d d	 | � } t j | � } t	 j
 j t d | � } | j | � n  d S(
   u!   Draw an image with specied color.u   (u    u   )u   ,u   RGBi�   u   %s.pngN(   i�   i�   (   t   tuplet   replacet   splitt   intt   floatR   t   newR   t   Drawt   ost   patht   joint	   IMAGE_DIRt   save(   t   color_rgb_tuple_strt
   color_namet   xt   color_rgb_tuplet   imaget   drawt
   image_file(    (    s   fdi_generator.pyt   save_color_imageu   s    Fc         C� sg   g  |  j  d d � j  d d � j d � D] } t | � ^ q( \ } } } t | | d | d d � S(   u�  
    Convert RGB to single RGB integer value.

    [Parameters]
        rgb_tuple_str: This kind of format: '(147,112,219)'

    [Return]
        rgb_value:  14381203
                    (
                        147
                        + (112 * 256)
                        + (219 * 256 * 256)
                    )

        RGB value= Red + (Green*256) + (Blue*256*256)
        (https://msdn.microsoft.com/en-us/library/dd355244.aspx)
    u   (u    u   )u   ,i   (   R   R   R   R   (   t   rgb_tuple_strR   t   r_valuet   g_valuet   b_value(    (    s   fdi_generator.pyt   rgb_to_rgb_value�   s    Fc   	      C� s=  g  } x|  D]� } g  | D] } t  | � ^ q } x� t | � D]� \ } } | t k rd d | | <q? t | k  o{ t k  n r� t t t � � | | <q? | t k r� t t t � � | | <q? t t | � � | | <q? W| j d j g  | D] } t	 | � ^ q� � � q Wt
 | d � � } | j d j | � � Wd QXd S(   u`   Processing raw data, apply [MIN_LIMIT, MAX_LIMIT] rule.
    Title line was already removed.
    i    u   , u   wu   
N(   R   t	   enumeratet   IGNORE_LIMITt	   MIN_LIMITR   t   roundt	   MAX_LIMITt   appendR   t   strt   opent   write(	   t   raw_matrix_without_titlet	   data_filet   out_listt
   each_tupleR   t   number_listt   it   numbert   f_out(    (    s   fdi_generator.pyt   processing_raw_data�   s    3c         C� sN  g  } t  |  d � �8 } g  | j �  D] } | j �  r% | j �  ^ q% } Wd QXx� t | � D]� \ } }	 | j d | d � g  |	 j d � D] } t | � ^ q� }
 t |
 � } xW t |
 � D]I \ } } | r� | j t | | | | t	 | j
 | | � � f � q� q� W| j d � q\ Wt  | d � � } | j d j | � � Wd QXd S(   u   Generate info_file.u   rNu	   Hap_%d:

i   u   ,u   
u   w(   R*   t	   readlinest   stripR#   R(   R   R   t   sumt   INFO_LINE_STYLER)   t   getR+   R   (   R-   t	   info_filet	   name_listt
   color_dictR.   t   f_inR   t   linesR1   t   linet   num_listt   num_sumt   jt   numR3   (    (    s   fdi_generator.pyt   generate_info_file�   s    7(%t	   HandleFdic           B� s2   e  Z d  Z d �  Z d �  Z d �  Z d �  Z RS(   u�   
    Modify fdi file to draw color.

    info_file was generated after HandleColorInfo()

    >>> hf = HandleFdi(fdi_file, info_file, out_file)
    >>> hf.parse_info_file()
    >>> hf.parse_fdi_file()
    >>> hf.write_to_file()
    c         C� s1   | |  _  | |  _ i  |  _ | |  _ g  |  _ d  S(   N(   R:   t   out_filet	   info_dictt   fdi_filet
   final_list(   t   selfRH   R:   RF   (    (    s   fdi_generator.pyt   __init__�   s
    				c   
      C� s*  d } t  �  } t |  j d � �8 } g  | j �  D] } | j �  r1 | j �  ^ q1 } Wd QXx� | D]� } | j d � r� | j d � } g  |  j | <qb g  | j �  j d � D] } | j �  r� | j �  ^ q� \ } } }	 | | k rt	 |	 | � | j
 | � n  |  j | j | t |	 � g � qb Wd S(   u�  
        Parse infomation file and extract TAXON_PIE_FREQUENCY and RGB color.

        [Return]
            {
                'Hap_1': [['1 /  1:', 17919]],
                ...,
                'Hap_5': [
                             ['1 /  3:', 11394815],
                             ['1 /  3:', 2763429],
                             ['1 /  3:', 16776960]
                         ],
                ...
            }
        u    u   rNu   Hap_u   :u   |(   t   setR*   R:   R5   R6   t
   startswitht   rstripRG   R   R   t   addR(   R"   (
   RJ   t   temp_hap_namet   exists_color_setR=   R   R>   R?   t   num_rawt   nameR   (    (    s   fdi_generator.pyt   parse_info_file�   s    	7'c         C� s[  t  |  j d � � } | j �  } Wd QXx-| D]%} | j d � rh | j d t � } |  j j | � q. | j d � r� | j d t � } |  j j | � q. | j d � rCd } | j	 d	 � \ } } | j	 d
 � d j d d � j
 �  } |  j | } d }	 |	 | j d	 � 7}	 x t | � D]q \ }
 \ } } | j	 d � d j
 �  } | t | � 7} |	 d |
 d | f d |
 d | f d |
 d 7}	 qW|	 d d t d d 7}	 y* t j |	 � d } t j |	 � d } Wn t k
 r�t j d � n X|	 j | d t | f � }	 |	 j | d t | f � }	 |  j j |	 � q. |  j j | � q. Wd S(   uG   
        Parse fdi file and save modified lines to final list.
        u   rNu   MIN_CIRC_RADIUSu   4u   MAX_CIRC_RADIUSu   50u   TAXON_NAME;H_i    u   TAXON_COLOR_PIE1u   ;i   u   Hu   Hapu    u   /u   TAXON_COLOR_PIE%d;%s;u   TAXON_PIE_FREQUENCY%d;%s;u   TAXON_STYLE_PIE%d;SOLID;u   TAXON_LINE_WIDTH;1;u   TAXON_LINE_COLOR;%s;u   TAXON_LINE_STYLE;SOLID;u   TAXON_ACTIVE;TRUE
u   Invalid fdi fileu   %s;%d;(   R*   RH   R5   RM   R   t   MIN_CIRC_RADIUSRI   R(   t   MAX_CIRC_RADIUSR   R6   RG   RN   R#   R   t   BORDER_COLORt   RE_TAXON_FREQUENCYt   findallt   RE_TAXON_ORIG_FREQUENCYt
   IndexErrort   syst   exitt   TAXON_FREQUENCY_STRt   TAXON_ORIG_FREQUENCY_STR(   RJ   R=   R>   R?   t   freq_sumt	   keep_partt   _t   hap_numt	   info_listt   modified_lineR1   RR   t	   rgb_valuet	   frequencyt   taxon_freq_strt   taxon_orig_freq_str(    (    s   fdi_generator.pyt   parse_fdi_file�   sN    %#	c         C� sM   t  j j t |  j � } t | d � �  } | j d j |  j � � Wd QXd S(   u   Write new fdi lines to file.u   wu    N(   R   R   R   t   OUT_DIRRF   R*   R+   RI   (   RJ   RF   R3   (    (    s   fdi_generator.pyt   write_to_file6  s    (   t   __name__t
   __module__t   __doc__RK   RT   Rj   Rl   (    (    (    s   fdi_generator.pyRE   �   s
   
		&	9c         C� s4   t  |  | | � } | j �  | j �  | j �  d S(   uL   Generate a new fdi with new proportions, new colors and new size limit.
    N(   RE   RT   Rj   Rl   (   RH   R:   RF   t   fdi(    (    s   fdi_generator.pyt   generate_new_fdi=  s    

t   XlsxFilec           B� s    e  Z d  Z d �  Z d �  Z RS(   u;   
    Handel xlsx files and return a matrix of content.
    c         C� s�   y t  j | � |  _ Wn� t  j j j k
 rR } t j d | � t j	 d � nc t
 k
 r� } t j d | | f � t j	 d � n- t k
 r� } t j | � t j	 d � n X|  j j |  _ |  j j |  _ g  |  _ |  j �  d  S(   Nu   Invalid xlsx format.
%si   u   No such xlsx file: %s. (%s)(   t   openpyxlt   load_workbookt   wbt   utilst
   exceptionst   InvalidFileExceptiont   loggingt   errorR\   R]   t   IOErrort   BaseExceptiont   activet   wst   titlet   ws_titlet   matrixt   _get_matrix(   RJ   t
   excel_filet   e(    (    s   fdi_generator.pyRK   J  s    	c         C� sp   xi t  |  j j � D]U \ } } g  } x* t  | � D] \ } } | j | j � q2 W|  j j t | � � q Wd S(   u0   Get a two dimensional matrix from the xlsx file.N(   R#   R~   t   rowsR(   t   valueR�   R
   (   RJ   R1   t   rowt   row_containert   cell(    (    s   fdi_generator.pyR�   ^  s
    (   Rm   Rn   Ro   RK   R�   (    (    (    s   fdi_generator.pyRr   F  s   	t   ColorChooseFramec           B� s\   e  Z d  Z d	 g  d � Z d �  Z d �  Z d �  Z d �  Z d �  Z	 d �  Z
 d �  Z RS(
   u�   Inner frame used for generating buttons and labels dynamically.

    Usage:
        >>> app = ColorChooseFrame(name_list=['SpeciesA', 'SpeciesB',
        >>>                                   'SpeciesC'])
        >>> app.mainloop()
    c         C� sv   t  j j |  | � | |  _ i  |  _ g  |  _ g  |  _ g  |  _ |  j �  |  j	 �  |  j
 �  |  j �  |  j �  d  S(   N(   t   tkt   FrameRK   R;   t   choosed_color_dictt   name_lebelst   buttonst   colored_bg_labelst	   set_stylet   create_widgetst   grid_configt   row_and_column_configt   bind_function(   RJ   t   masterR;   (    (    s   fdi_generator.pyRK   o  s    					



c         C� s#   t  j �  } | j d d d �d S(   u   Set custom style for widget.u   color.TButtont   paddingi    N(   R   t   Stylet	   configure(   RJ   t   s(    (    s   fdi_generator.pyR�   �  s    c         C� s�   x} |  j  D]r } |  j j t j |  j d | �� |  j j t j |  j d t d d �� |  j	 j t j |  j d d �� q
 Wd S(   u�  Create widgets for dynamically color choose pane
        +------------------------------------------------+
        |                                                |
        |                                                |
        +------------------------------------------------+
        |   NAME_1    BUTTON    COLORED_BACKGROUND_LABEL |
        |   NAME_2    BUTTON    COLORED_BACKGROUND_LABEL |
        |   NAME_3    BUTTON    COLORED_BACKGROUND_LABEL |
        |   ...       ...       ...                      |
        |   NAME_n    BUTTON    COLORED_BACKGROUND_LABEL |
        +------------------------------------------------+
        |                                                |
        +------------------------------------------------+
        t   textt   styleu   color.TButtont
   backgroundu   #FFFFFFN(
   R;   R�   R(   R   t   LabelR�   R�   t   Buttont   CHOOSE_COLOR_BUTTON_TEXTR�   (   RJ   RS   (    (    s   fdi_generator.pyR�   �  s    "
c         C� s�   x t  |  j � D]n \ } } | j d | d d d d � |  j | j d | d d d d � |  j | j d | d d d d � q Wd S(	   u4   Grid configurations

        Three columns.
        R�   t   columni    t   stickyu   wei   i   N(   R#   R�   t   gridR�   R�   (   RJ   R1   RS   (    (    s   fdi_generator.pyR�   �  s    #c         C� sg   x3 t  |  j � D]" \ } } |  j j | d d �q Wx* t d � D] } |  j j | d d �qC Wd S(   u   Row and column configurationst   weighti    i   i   N(   R#   R�   R�   t   rowconfiguret   ranget   columnconfigure(   RJ   R1   RS   (    (    s   fdi_generator.pyR�   �  s    c         � sG   x@ t  �  j � D]/ \ } } �  j | } | �  f d � | d <q Wd S(   u�   Bind functions to each button.

        Use defualt parameter in lambda function to avoid variable bug:
        If no default paramter, value of i will always be value of the last i
        button['command'] = lambda i=i: self._ask_color(i)
        c         � s   �  j  |  � S(   N(   t
   _ask_color(   R1   (   RJ   (    s   fdi_generator.pyt   <lambda>�  s    u   commandN(   R#   R�   R�   (   RJ   R1   t   labelt   button(    (   RJ   s   fdi_generator.pyR�   �  s    c         C� sx   t  �  } | d s d S| d |  j |  j | <|  j | j d d t | d � t | d � f d | d d d � d S(	   u"   Popup a color pane to choose colori    NR�   u   %17s %8si   R�   t   fontu	   Monospace(   R   R�   R;   R�   t   configR)   (   RJ   R1   t   color(    (    s   fdi_generator.pyR�   �  s    	
$
c         C� s^   x |  j  D] } | j �  q
 Wx |  j D] } | j �  q( Wx |  j D] } | j �  qF Wd S(   uL   Destroy all name_labels, buttons and color_labels to show new ones.
        N(   R�   t   destroyR�   R�   (   RJ   t
   name_labelR�   t   color_label(    (    s   fdi_generator.pyt   destroy_all_inner_widgets�  s    N(   Rm   Rn   Ro   t   NoneRK   R�   R�   R�   R�   R�   R�   R�   (    (    (    s   fdi_generator.pyR�   g  s   			
	
		t   Appc           B� s�   e  Z d d  � Z d �  Z d �  Z d �  Z d �  Z d �  Z d �  Z	 d �  Z
 d �  Z d	 �  Z d
 �  Z d �  Z d �  Z d �  Z d �  Z d �  Z RS(   c         C� s�   t  j j |  | � g  |  _ g  |  _ d |  _ d |  _ d  |  _ |  j	 j
 t � |  j	 j t � |  j �  |  j �  |  j �  |  j �  |  j �  d  S(   Nu    (   R�   R�   RK   R;   t   excel_matrixt
   excel_namet   fdi_nameR�   t   dynamic_areaR�   t   geometryt   DEFAULT_GEOMETRYR   t	   APP_TITLER�   R�   R�   R�   t   bind_functions(   RJ   R�   (    (    s   fdi_generator.pyRK   �  s    					



c         C� su   t  j �  } | j d d d �| j d d d �| j d d d �| j d	 d d d d
 �| j d d d �d S(   u   Set custom style for widget.u   TButtonR�   i   i
   u   execute.TButtont
   foregroundu   redu   TLableu   status.TLabelu   #2E64FEu   TEntryN(   i   i
   (   i   i
   (   i   i
   (   R   R�   R�   (   RJ   R�   (    (    s   fdi_generator.pyR�   �  s    c         C� s�  t  j |  j d d �|  _ t  j |  j d d �|  _ t  j |  j d d �|  _ t  j |  j d t �|  _ t  j	 |  j d t
 �|  _ t j �  |  _ t  j |  j d |  j d d �|  _ |  j j t � t  j |  j d t �|  _ t  j	 |  j d t �|  _ t j �  |  _ t  j |  j d |  j �|  _ |  j j t � t  j |  j d t �|  _ t  j |  j � |  _ t  j |  j d t �|  _ t  j |  j � |  _ t  j |  j d t  �|  _! t  j |  j � |  _" t  j |  j d t# �|  _$ t  j |  j � |  _% t  j |  j d t& �|  _' t  j |  j � |  _( t  j |  j d t) �|  _* t  j |  j � |  _+ t  j |  j d t, �|  _- t  j |  j � |  _. t  j |  j d t/ �|  _0 t  j |  j � |  _1 |  j j2 d t3 � |  j j2 d t4 � |  j" j2 d t5 � |  j% j2 d t6 � |  j( j2 d t7 � |  j+ j2 d t8 � |  j. j2 d t9 � |  j1 j2 d t: � t; |  j d |  j< �|  _= t  j	 |  j d t> d d	 �|  _? t j �  |  _@ t  j |  j d |  j@ d d
 �|  _A d S(   u�  Create GUI widgets.
        +------------------------------------------------+
        |                                                |
        |                                                |
        +------------------------------------------------+
        |   NAME_1    BUTTON    COLORED_BACKGROUND_LABEL |
        |   NAME_2    BUTTON    COLORED_BACKGROUND_LABEL |
        |   NAME_3    BUTTON    COLORED_BACKGROUND_LABEL |
        |   ...       ...       ...                      |
        |   NAME_n    BUTTON    COLORED_BACKGROUND_LABEL |
        +------------------------------------------------+
        |                                                |
        +------------------------------------------------+
        R�   i   R�   t   textvariableR�   u   config.TLabelu   0R;   u   execute.TButtonu   status.TLabelN(B   R   R�   R�   t   config_panet   color_choose_panet   execute_paneR�   t   CHOOSE_EXCEL_LABEL_TEXTt   choose_excel_labelR�   t   CHOOSE_EXCEL_BUTTON_TEXTt   choose_excel_buttonR�   t	   StringVart   display_excel_vart   display_excel_labelRL   t   DEFALT_CHOOSE_EXCEL_LABEL_TEXTt   CHOOSE_FDI_LABEL_TEXTt   choose_fdi_labelt   CHOOSE_FDI_BUTTON_TEXTt   choose_fdi_buttont   display_fdi_vart   display_fdi_labelt   DEFALT_CHOOSE_FDI_LABEL_TEXTt   OUTPUT_FILE_LABEL_TEXTt   output_file_labelt   Entryt   output_file_entryt   IGNORE_LIMIT_LABEL_TEXTt   ignore_limit_labelt   ignore_limit_entryt   MIN_LIMIT_LABEL_TEXTt   min_limit_labelt   min_limit_entryt   MAX_LIMIT_LABEL_TEXTt   max_limit_labelt   max_limit_entryt   MIN_CIRC_RADIUS_LABEL_TEXTt   min_circ_radius_labelt   min_circ_radius_entryt   MAX_CIRC_RADIUS_LABEL_TEXTt   max_circ_radius_labelt   max_circ_radius_entryt   BORDER_COLOR_LABEL_TEXTt   border_color_labelt   border_color_entryt   INFO_LINE_STYLE_LABEL_TEXTt   info_line_style_labelt   info_line_style_entryt   insertt   DEFAULT_OUTPUT_FILER$   R%   R'   RU   RV   RW   R8   R�   R;   R�   t   EXECUTE_BUTTON_TEXTt   execute_buttont
   status_vart   status_label(   RJ   (    (    s   fdi_generator.pyR�   �  sz    		c      	   C� s�  |  j  j �  |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j	 j d d d d d d � |  j
 j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d	 d d d d � |  j j d d	 d d d d � |  j j d d
 d d d d � |  j j d d
 d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d � |  j j d d d d d d	 d d � |  j j d d d d d d	 d d � |  j j d d d d d d	 d d � d S(   u   Grid configurationsR�   i    R�   R�   u   wensi   i   u   wei   i   i   i   i   i   i	   t
   columnspanN(   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   (   RJ   (    (    s   fdi_generator.pyR�   b  s:    %%c         C� s�  |  j  j d d d �|  j  j d d d �|  j  j d d d �|  j  j d d d �x* t d � D] } |  j j | d d �qe Wx0 t d � D]" } |  j j | d d d d �q� Wx3 t |  j � D]" \ } } |  j j | d d �q� Wx0 t d � D]" } |  j j | d d d d �q� W|  j j d d d �|  j j d d d �x0 t d � D]" } |  j j | d d d d �qZWd S(	   u   Row and column configurationsi    R�   i   i   i   t   uniformu   fredN(	   R�   R�   R�   R�   R�   R#   R;   R�   R�   (   RJ   R1   RS   (    (    s   fdi_generator.pyR�   �  s       c         C� s4   |  j  |  j d <|  j |  j d <|  j |  j d <d S(   u   Bind functions to buttonsu   commandN(   t   _read_excel_fileR�   t   _read_fdi_fileR�   t   _executeR�   (   RJ   (    (    s   fdi_generator.pyR�   �  s    c         C� s�   t  j d d g � |  _ |  j s% d S|  j j t j j |  j � � |  j t	 t j j |  j � � t
 |  j � j |  _ |  j �  r� t |  j d � |  _ |  j |  j d � n  d S(   u   Select and read excel filet	   filetypesu
   Xlsx filesu   xlsxNi    (   u
   Xlsx filesu   xlsx(   t   tkFileDialogt   askopenfilenameR�   R�   RL   R   R   t   basenamet   _set_status_var_textt   CHOOSED_XLSX_FILERr   R�   R�   t   _validate_excel_matrixt   listR;   t   refresh_dynamic_area(   RJ   (    (    s   fdi_generator.pyR�   �  s    			c         C� s�   t  j d d g � } | s d S| |  _ |  j j t j j |  j � � |  j t	 t j j |  j � � |  j
 j d d � |  j
 j d t j j |  j � � d S(   u   Select and read fdi fileR�   u	   Fdi filesu   fdiNu   0u   end(   u	   Fdi filesu   fdi(   R�   R�   R�   R�   RL   R   R   R�   R�   t   CHOOSED_FDI_FILER�   t   deleteR�   (   RJ   t   filename(    (    s   fdi_generator.pyR�   �  s    			c         C� s�   t  |  j j �  � a t  |  j j �  � a t  |  j j �  � a t |  j	 j �  � a
 t |  j j �  � a t |  j j �  � a t |  j j �  � a d  S(   N(   R   R�   R9   R$   R�   R%   R�   R'   R)   R�   RU   R�   RV   R�   RW   R�   R8   (   RJ   (    (    s   fdi_generator.pyt   _read_configs�  s    	c         C� s�   |  j  �  r� y� |  j �  t |  j d t � |  j t � t t t |  j	 |  j
 j � |  j t � |  j j �  j �  } t |  j t | � |  j t � |  j d t j j | � � Wq� t k
 r� } |  j d | � q� Xn  d S(   u   Do validation and executioni   u    Done!  Output file:  ./output/%su   ERRORN(   t   _check_paramsR  R4   R�   t   PROCESSING_DATA_FILER�   t   RAW_DATA_PROCESSED_INFORD   t	   INFO_FILER;   R�   R�   t   INFO_FILE_PROCESSED_INFOR�   R9   R6   Rq   R�   t   FDI_FILE_GENERATED_INFOR   R   R�   t	   Exceptiont   _display_error(   RJ   RF   R�   (    (    s   fdi_generator.pyR�   �  s"    
	c         C� s�   |  j  t � |  j s* |  j t t � t S|  j sG |  j t t	 � t S|  j
 sd |  j t t � t St |  j � t |  j j � k r� |  j t t � t S|  j j �  j �  } | s� |  j t t � t S|  j �  s� t S|  j  t � t S(   u*   Validate files and contents before running(   R�   t   STARTING_VALIDATING_DATA_INFOR�   R	  t   NO_XLSX_FILE_ERROR_TITLEt   NO_XLSX_FILE_ERROR_MESSAGEt   FalseR�   t   NO_FDI_FILE_ERROR_TITLEt   NO_FDI_FILE_ERROR_MESSAGER�   t   INVALID_XLSX_FILE_ERROR_TITLEt   INVALID_XLSX_FILE_ERROR_MESSAGEt   lenR;   R�   R�   t!   NOT_ALL_COLOR_CHOOSED_ERROR_TITLEt#   NOT_ALL_COLOR_CHOOSED_ERROR_MESSAGER�   R9   R6   t   NO_OUTFILE_ERROR_TITLEt   NO_OUTFILE_ERROR_MESSAGEt"   _validate_xlsx_consistent_with_fdit   FINISHED_VALIDATING_DATA_INFOt   True(   RJ   RF   (    (    s   fdi_generator.pyR  �  s>    			!c         C� s�  g  |  j  D] } t | � ^ q
 } t t | � � d k rN |  j t t � t Sx� t |  j  d � D]� \ } } y t | � WnC t	 k
 r� qb qb t
 k
 r� |  j t t d | d f � t SX|  j t t d | d f � t Sqb Wx� t |  j  d � D]� \ } } x� t | � D]� \ } } y t | � Wqt	 k
 re|  j t t | d | d f � t St
 k
 r�|  j t t | d | d f � t SXqWq� Wt S(   u   Validate content of xlsx filei   i    i   (   R�   R  RL   R	  R  R  R  R#   R   t
   ValueErrort	   TypeErrort   BLANK_CELL_ERROR_TITLEt   BLANK_CELL_ERROR_MESSAGEt   XLSX_FIRST_LINE_ERROR_TITLEt   XLSX_FIRST_LINE_ERROR_MESSAGEt   XLSX_NOT_FIRST_LINE_ERROR_TITLEt!   XLSX_NOT_FIRST_LINE_ERROR_MESSAGER  (   RJ   R/   t   each_tuple_len_listR1   R�   RB   (    (    s   fdi_generator.pyR�   0  sH      c         C� s�   t  |  j d � � } | j �  } Wd QXt j d � } | j | � } t t | � � t t |  j � � t | � t |  j � d k r� |  j	 t
 t � t St S(   u;   Check if data numbers is in accordance with fdi Hap numbersu   rNu   TAXON_NAME;H_.*i   (   R*   R�   t   readt   ret   compileRY   t   printR  R�   R	  t.   XLSX_DATA_AND_FDI_HAP_NUMBER_DISCORDANCE_TITLEt0   XLSX_DATA_AND_FDI_HAP_NUMBER_DISCORDANCE_MESSAGER  R  (   RJ   R=   t   contentt   re_hap_numberst	   hap_lines(    (    s   fdi_generator.pyR  e  s    c         C� s!   |  j  j | � |  j j �  d S(   u#   Display information on status labelN(   R�   RL   R�   t   update_idletasks(   RJ   R�   (    (    s   fdi_generator.pyR�   u  s    c         C� s+   d | } |  j  | � t j | | � d S(   u2   Display information on status label and messageboxu   ERROR: N(   R�   t   tkMessageBoxt	   showerror(   RJ   R   t   message(    (    s   fdi_generator.pyR	  z  s    
c      
   C� s�   |  j  j �  |  j  j �  t |  j | � |  _  x? t | � D]1 \ } } |  j  j d | d d d d d d � q< W|  j  j �  d S(	   uz   Dynamically refresh color choose area.
        Generate new buttons and labels according to number of categories.
        R�   R�   i    R�   i   R�   u   wensN(   R�   R�   R�   R�   R�   R#   R�   R,  (   RJ   t   new_name_listR1   RS   (    (    s   fdi_generator.pyR�   �  s    	N(   Rm   Rn   R�   RK   R�   R�   R�   R�   R�   R�   R�   R  R�   R  R�   R  R�   R	  R�   (    (    (    s   fdi_generator.pyR�   �  s    		g	2							6	5			c          C� s   t  �  }  |  j �  d S(   u   Main GUI functionN(   R�   t   mainloop(   t   app(    (    s   fdi_generator.pyt   main�  s    	u   __main__(p   Ro   t
   __future__R    R   R   R\   R   R�   R   R$  Rs   Ry   t   PILR   R   R   t   colorsyst   ImportErrorR�   t   versiont   TkinterR�   R   R�   t   tkColorChooserR   R-  t   tkinterR   R	   t   tkinter.colorchoosert   __version__t
   __auther__R$   R%   R'   RU   RV   RW   R8   R^   R_   R%  RX   RZ   t   abspathRk   R   t   INFO_DIRt   each_dirt   isdirt   mkdirR   R  R  R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R�   R  R  R  R  R  R  R  R  R  R  R  R  R  R  R   R!  R'  R(  R
  R  R  R  R  R   R"   R4   RD   t   objectRE   Rq   Rr   R�   R�   R�   R3  Rm   (    (    (    s   fdi_generator.pyt   <module>   s�   

				x		!m� �	